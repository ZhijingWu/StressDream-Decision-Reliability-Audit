"""Verify retained CSV/JSON measurements and public hashes; no model or dynamics execution."""
from pathlib import Path
from hashlib import sha256
import csv
import json
import math
import statistics

ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def rows(name):
    with (ROOT/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def close(a,b):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12),(a,b)
def percentile(values,p):
    v=sorted(values);i=(len(v)-1)*p;lo=math.floor(i);hi=math.ceil(i)
    return v[lo]+(i-lo)*(v[hi]-v[lo])

def verify():
    manifest=load('reproducibility/evidence_manifest.json')
    for item in manifest['files']:
        p=ROOT/item['path'];assert p.is_file(),item['path']
        assert sha256(p.read_bytes()).hexdigest()==item['sha256'],item['path']
    context=[r for r in rows('experiments/gate0/raw/CONTEXT_SUMMARY.csv') if r['split']=='test']
    pair=[r for r in rows('experiments/gate0/raw/PAIRWISE_ACTION_DIFFERENCES.csv') if r['split']=='test']
    assert len(context)==16 and sum(float(r['spread_m2'])>.005 for r in context)==12
    assert len(pair)==160 and sum(float(r['absolute_difference_m2'])>.005 for r in pair)==106
    actions=[r for r in rows('experiments/gate0/ACTION_SEPARATION_RESULTS.csv') if r['split']=='test' and r['action_id']=='A0']
    close(max(float(r['robust_regret_m2']) for r in actions),.000176067136293)
    b=load('experiments/gate0b/raw/HELDOUT_SUMMARY.json')
    contexts=rows('experiments/gate0b/raw/HELDOUT_CONTEXT_SUMMARY.csv')
    assert len(contexts)==b['contexts']==64
    assert sum(float(r['utility_spread_m2'])>.005 for r in contexts)==b['informative_contexts']['0.005']==43
    assert sum(float(r['top_runner_up_gap_m2'])>.005 for r in contexts)==b['meaningful_unique_optimum_contexts']['0.005']==41
    assert sum(int(r['safe_action_count'])==0 for r in contexts)==b['no_safe_contexts']==21
    assert len([n for n in b['singleton_optimum_counts'].values() if n>0])==5
    close(statistics.mean(float(r['A0_task_regret_m2']) for r in contexts),b['best_constant_mean_regret_m2'])
    close(b['best_constant_mean_regret_m2'],.10308741772432242)
    record=rows('experiments/gate1a/READOUT_RESULTS.csv')
    summary=load('experiments/gate1a/raw/READOUT_SUMMARY.json')
    fig=load('note/evidence/FIGURE_MEASUREMENTS.json')
    # Domain names are recorded unchanged in the retained CSV.
    p95={}
    for domain,key,figure_key in [('clean','validation_clean','clean_p95_m2'),('reconstruction','validation_reconstruction','vae_p95_m2')]:
        selected=[r for r in record if r['split']=='validation' and r['domain']==domain]
        assert len(selected)==16 and all(r['status']=='ok' for r in selected)
        value=percentile([abs(float(r['C_error_m2'])) for r in selected],.95)
        close(value,summary[key]['abs_C_error_m2']['p95']);close(value,fig[figure_key]);p95[domain]=value
    values=rows('note/figures/readout_error_values.csv')
    close(float(values[0]['p95_absolute_safety_error_m2']),fig['clean_p95_m2'])
    close(float(values[1]['p95_absolute_safety_error_m2']),fig['vae_p95_m2'])
    count=load('experiments/gate1a/raw/COUNTERS.json')
    assert (count['future_latents'],count['paired_reconstructions'],count['denoiser_forwards'])==(43,32,215)
    assert load('experiments/gate1a/raw/COMPATIBILITY_PASS.json')['passed'] is True
    result={'public_hashes_verified':len(manifest['files']),'gate0_informative':12,'gate0_separated_pairs':106,
            'gate0b_contexts':64,'gate0b_informative':43,'gate0b_meaningful_unique':41,'gate0b_no_safe':21,
            'readout_p95_m2':p95,'new_dynamics_queries':0,'new_model_calls':0}
    print(json.dumps(result,indent=2))

if __name__=='__main__':verify()
