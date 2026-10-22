"""Plot retained Gate 1A measurements only. No scientific experiment execution."""
from pathlib import Path
import json,csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
F=Path(__file__).resolve().parent
data=json.loads((F.parent/'evidence/FIGURE_MEASUREMENTS.json').read_text(encoding='utf-8'))
errors=[data['clean_p95_m2'],data['vae_p95_m2']]
with (F/'readout_error_values.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['domain','p95_absolute_safety_error_m2','n','prespecified_margin_m2'])
    for domain,value in zip(['Clean renderer','VAE reconstruction'],errors):w.writerow([domain,repr(value),16,data['margin_m2']])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':10,'xtick.labelsize':9.5,'ytick.labelsize':10,'pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(6.7,1.9))
ax.barh([1,0],errors,height=.48,color=['.35','.7'],edgecolor='black',linewidth=.55)
ax.axvline(data['margin_m2'],color='black',linestyle='--',linewidth=.9)
ax.text(data['margin_m2']+.00012,1.47,'Prespecified margin: 0.005',ha='left',va='center',fontsize=9)
for y,e in zip([1,0],errors):ax.text(e+.00014,y,f'{e:.8f}',va='center',fontsize=9.5)
ax.set_yticks([1,0],['Clean renderer','VAE reconstruction'])
ax.set_xlim(0,.0115);ax.set_ylim(-.5,1.75)
ax.set_xticks([0,.002,.004,.006,.008,.010],[f'{x:.3f}' for x in [0,.002,.004,.006,.008,.010]])
ax.set_xlabel(r'p95 absolute safety-score readout error ($\mathrm{m}^2$)',labelpad=5)
ax.spines[['top','right']].set_visible(False)
ax.tick_params(axis='y',length=0)
fig.subplots_adjust(left=.265,right=.985,top=.94,bottom=.30)
for suffix in ['pdf','png']:fig.savefig(F/f'readout_error.{suffix}',dpi=300,bbox_inches='tight',pad_inches=.03)
plt.close(fig)
