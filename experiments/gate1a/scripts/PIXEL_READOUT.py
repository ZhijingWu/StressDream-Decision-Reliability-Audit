"""Pixel-only geometry reader; constants fit on tuning images, never test labels.

No learned-head, latent, simulator state or trajectory is accepted by read().
Calibration estimates geometric offsets and chooses a grayscale threshold.
"""
import numpy as np,math

def circular(x):return np.arctan2(np.sin(x),np.cos(x))

def feature(rgb,threshold):
    if np.asarray(rgb).shape!=(128,128,3):return {'status':'wrong_shape'}
    gray=np.asarray(rgb,dtype=np.float64).mean(axis=2)
    mask=gray<threshold;seen=np.zeros(mask.shape,dtype=bool);components=[]
    for row,col in np.argwhere(mask):
        if seen[row,col]:continue
        seen[row,col]=True;stack=[(int(row),int(col))];pixels=[]
        while stack:
            v,u=stack.pop();pixels.append((v,u))
            for dv in [-1,0,1]:
                for du in [-1,0,1]:
                    vv,uu=v+dv,u+du
                    if 0<=vv<128 and 0<=uu<128 and mask[vv,uu] and not seen[vv,uu]:
                        seen[vv,uu]=True;stack.append((vv,uu))
        if len(pixels)>=5:components.append(pixels)
    components.sort(key=len,reverse=True)
    if not components:return {'status':'no_dark_component'}
    pix=np.array(components[0]);area=len(pix)
    if area<12 or area>600:return {'status':'area_out_of_range','area':area}
    if len(components)>1 and len(components[1])>.35*area:return {'status':'multiple_components','area':area}
    if np.ptp(pix[:,0])>40 or np.ptp(pix[:,1])>40:return {'status':'component_extent','area':area}
    weights=(threshold-gray[pix[:,0],pix[:,1]])/threshold
    xy=np.column_stack([3*((pix[:,1]+.5)/128-.5),3*(.5-(pix[:,0]+.5)/128)])
    weights/=weights.sum();center=(xy*weights[:,None]).sum(axis=0)
    centered=xy-center;cov=(centered*weights[:,None]).T@centered
    values,vectors=np.linalg.eigh(cov);axis=vectors[:,1]
    ratio=float(values[1]/max(values[0],1e-15));projection=centered@axis
    skew=float(np.sum(weights*projection**3)/max(values[1],1e-15)**1.5)
    if ratio<1.3 or abs(skew)<.05:return {'status':'heading_ambiguous','area':area,'axis_ratio':ratio,'skew':skew}
    if skew<0:axis=-axis
    return {'status':'ok','area':area,'axis_ratio':ratio,'skew':abs(skew),'cx':float(center[0]),'cy':float(center[1]),'raw_theta':float(np.arctan2(axis[1],axis[0]))}

def calibrate(images,labels):
    # images includes 16 tuning states x paired clean/reconstructed domains only.
    options=[]
    for threshold in [64,96,128,160]:
        features=[feature(im,threshold) for im in images]
        valid=[i for i,f in enumerate(features) if f['status']=='ok']
        if len(valid)<8:continue
        angles=np.array([labels[i][2]-features[i]['raw_theta'] for i in valid])
        offset=float(np.arctan2(np.sin(angles).sum(),np.cos(angles).sum()))
        X=[];y=[]
        for i in valid:
            f=features[i];a=f['raw_theta']+offset;c,s=math.cos(a),math.sin(a)
            X.extend([[1,0,c,-s],[0,1,s,c]])
            y.extend([labels[i][0]-f['cx'],labels[i][1]-f['cy']])
        correction=np.linalg.lstsq(np.array(X),np.array(y),rcond=None)[0]
        params={'threshold':threshold,'angle_offset':offset,'position_correction':correction.tolist(),'area_bounds':[12,600],'axis_ratio_min':1.3,'skew_abs_min':.05,'secondary_component_fraction_max':.35,'extent_max_px':40,'tuning_images':len(images),'tuning_parseable':len(valid)}
        errors=[];heading=[]
        for i in valid:
            r=read(images[i],params);errors.append(float(np.linalg.norm(np.array([r['x'],r['y']])-np.array(labels[i][:2]))))
            heading.append(float(abs(circular(r['theta']-labels[i][2]))))
        objective=float(np.mean(np.square(errors))+.01*np.mean(np.square(heading))+(len(images)-len(valid))/len(images))
        params.update(tuning_position_max_m=max(errors),tuning_heading_max_rad=max(heading),selection_objective=objective)
        options.append(params)
    if not options:raise RuntimeError('No readout threshold had enough tuning parses; no validation retuning allowed')
    return min(options,key=lambda p:p['selection_objective']),options

def read(rgb,params):
    f=feature(rgb,params['threshold'])
    if f['status']!='ok':return f
    theta=float((f['raw_theta']+params['angle_offset'])%(2*np.pi))
    dx,dy,along,across=params['position_correction'];c,s=math.cos(theta),math.sin(theta)
    x=f['cx']+dx+along*c-across*s;y=f['cy']+dy+along*s+across*c
    f.update(x=float(x),y=float(y),theta=theta,C=float(x*x+y*y-.25**2),goal_distance_squared=float((x-1)**2+y*y))
    return f
