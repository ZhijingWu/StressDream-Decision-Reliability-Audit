"""Independent exhaustive CPU Dubins oracle. No torch, WM, renderer or repo import.

Branch id bit t: 0 => delta[t]=+1, 1 => delta[t]=-1 (LSB is time 0).
Q* = min_branch min_(t=0..H) (x_t**2+y_t**2-r**2); maximize Q* across actions.
All calculations use numpy.float64. 'Exact' means exhaustive finite discrete
support evaluated numerically, not certified exact-real arithmetic.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np

REVISION = "b16fa067d3d949ef09ad48a984c62ea8ecbbfe6d"
ACTION_IDS = ("A0", "A1", "A2", "A3", "A4")
NUMERIC_TOLERANCE = 1e-12


@dataclass(frozen=True)
class Dynamics:
    speed: float = 1.0
    dt: float = 0.05
    obstacle_radius: float = 0.25
    obstacle_x: float = 0.0
    obstacle_y: float = 0.0
    max_turn_rate: float = 1.25


def canonical_json(value):
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safety(states, dynamics=Dynamics()):
    s = np.asarray(states, dtype=np.float64)
    return ((s[..., 0] - dynamics.obstacle_x) ** 2
            + (s[..., 1] - dynamics.obstacle_y) ** 2
            - dynamics.obstacle_radius ** 2)


def disturbance_sequences(horizon):
    if not isinstance(horizon, int) or not 1 <= horizon <= 16:
        raise ValueError("This small exhaustive oracle supports integer H in [1,16].")
    ids = np.arange(1 << horizon, dtype=np.uint32)
    bits = (ids[:, None] >> np.arange(horizon, dtype=np.uint32)) & 1
    return (1 - 2 * bits.astype(np.int8)).astype(np.int8)


def branch_probabilities(disturbances, p):
    if not 0 < p < 1:
        raise ValueError("Support comparison requires 0 < p < 1.")
    d = np.asarray(disturbances)
    flips = np.sum(d == -1, axis=1)
    return (np.float64(p) ** flips
            * np.float64(1.0 - p) ** (d.shape[1] - flips))


def _validate(state, actions, dynamics):
    state = np.asarray(state, dtype=np.float64)
    actions = np.asarray(actions, dtype=np.float64)
    if state.shape != (3,) or actions.ndim != 1:
        raise ValueError("State must be (3,), actions must be one-dimensional.")
    if not np.all(np.isfinite(state)) or not np.all(np.isfinite(actions)):
        raise ValueError("Inputs must be finite.")
    if np.any(np.abs(actions) > dynamics.max_turn_rate):
        raise ValueError("Angular rate exceeds the declared action bounds.")
    if dynamics.speed <= 0 or dynamics.dt <= 0 or dynamics.obstacle_radius <= 0:
        raise ValueError("Invalid physical constants.")
    return state, actions


def replay(state, actions, disturbances, dynamics=Dynamics()):
    """One witness; positions use PRE-update heading. No heading wrap needed."""
    state, actions = _validate(state, actions, dynamics)
    disturbances = np.asarray(disturbances)
    if disturbances.shape != actions.shape or not np.all(np.isin(disturbances, [-1, 1])):
        raise ValueError("A matching +/-1 disturbance vector is required.")
    path = np.empty((len(actions) + 1, 3), dtype=np.float64)
    path[0] = state
    for t, (a, delta) in enumerate(zip(actions, disturbances)):
        x, y, theta = path[t]
        path[t + 1] = (x + dynamics.speed * dynamics.dt * np.cos(theta),
                       y + dynamics.speed * dynamics.dt * np.sin(theta),
                       theta + dynamics.dt * np.float64(delta) * a)
    return path


def enumerate_query(state, actions, dynamics=Dynamics(), disturbances=None):
    """Return each branch's minimum safety and final state, plus a replayable argmin."""
    state, actions = _validate(state, actions, dynamics)
    ds = disturbance_sequences(len(actions)) if disturbances is None else np.asarray(disturbances)
    if ds.shape != (1 << len(actions), len(actions)) or not np.all(np.isin(ds, [-1, 1])):
        raise ValueError("Full binary disturbance support is required.")
    current = np.broadcast_to(state, (len(ds), 3)).copy()
    minima = np.full(len(ds), safety(state, dynamics), dtype=np.float64)
    times = np.zeros(len(ds), dtype=np.int16)
    min_x, min_y = current[:, 0].copy(), current[:, 1].copy()
    for t, a in enumerate(actions):
        # x/y must both use theta_t, not theta_(t+1).
        old_theta = current[:, 2].copy()
        current[:, 0] += dynamics.speed * dynamics.dt * np.cos(old_theta)
        current[:, 1] += dynamics.speed * dynamics.dt * np.sin(old_theta)
        current[:, 2] = old_theta + dynamics.dt * ds[:, t].astype(np.float64) * a
        values = safety(current, dynamics)
        lower = values < minima
        times[lower] = t + 1
        min_x[lower], min_y[lower] = current[lower, 0], current[lower, 1]
        minima = np.minimum(minima, values)
    witness_id = int(np.argmin(minima))  # deterministic first argmin in branch-id order
    path = replay(state, actions, ds[witness_id], dynamics)
    q = float(minima[witness_id])
    return dict(q_star=q, support_failure=bool(q <= 0.0),
                boundary_ambiguous=bool(abs(q) <= NUMERIC_TOLERANCE),
                branch_min_safety=minima, branch_min_time=times,
                min_positions=np.stack([min_x, min_y], axis=1), final_states=current,
                witness_id=witness_id, witness_delta=ds[witness_id].copy(),
                witness_path=path, witness_min_time=int(times[witness_id]))


def candidate_actions(horizon):
    if horizon not in (12, 16):
        raise ValueError("Frozen candidate designs exist only for H=12 or H=16.")
    half = horizon // 2
    return np.asarray([
        [0.0] * horizon,
        [0.625] * horizon,
        [1.25] * horizon,
        [1.25] * half + [0.0] * half,
        [0.0] * half + [1.25] * half,
    ], dtype=np.float64)


def frozen_config():
    contexts = []
    for rho in (0.35, 0.45, 0.60, 0.75):
        for beta in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
            contexts.append(dict(context_id=f"C{len(contexts):02d}",
                                 split="calibration" if beta in (0.2, 0.8) else "test",
                                 rho=rho, beta=beta, state=[-rho, 0.0, beta]))
    return dict(schema_version=1, source_revision=REVISION, dynamics=asdict(Dynamics()),
                dtype="float64", include_initial_state=True,
                time_update="position uses theta_t; heading updated afterwards",
                safety="C=(x-ox)^2+(y-oy)^2-r^2; unsafe C<=0; maximize min C",
                main_horizon=12, fallback_horizon=16,
                fallback_trigger="fewer than 8/16 test contexts have spread > 0.005 m^2",
                fallback_context_policy="same frozen 24 contexts; no reselection",
                thresholds_m2=[0.0025, 0.005, 0.01], numeric_tolerance=NUMERIC_TOLERANCE,
                probability_rates=[0.2, 0.4], contexts=contexts,
                actions={str(h): dict(zip(ACTION_IDS, candidate_actions(h).tolist())) for h in (12, 16)},
                distinct_sequence_note="2^H sign strings; inactive and final turns can yield duplicate safety paths",
                seed=None, gate1_authorized=False)


def dump_csv(path, rows):
    if not rows:
        raise ValueError("No rows.")
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_horizon(config, horizon, out):
    start = time.perf_counter()
    dynamics = Dynamics(**config["dynamics"])
    ds = disturbance_sequences(horizon)
    weights = {p: branch_probabilities(ds, p) for p in config["probability_rates"]}
    actions = np.asarray([config["actions"][str(horizon)][a] for a in ACTION_IDS], dtype=np.float64)
    results, pairs, contexts, witnesses, arrays = [], [], [], [], []
    max_witness_residual = 0.0
    for context in config["contexts"]:
        evaluated = [enumerate_query(context["state"], a, dynamics, ds) for a in actions]
        qs = np.asarray([x["q_star"] for x in evaluated], dtype=np.float64)
        best_q = float(qs.max())
        best_ids = [a for a, q in zip(ACTION_IDS, qs) if abs(best_q-q) <= NUMERIC_TOLERANCE]
        spread = float(np.ptp(qs))
        cr = dict(horizon=horizon, context_id=context["context_id"], split=context["split"],
                  rho=context["rho"], beta=context["beta"], spread_m2=spread,
                  best_action=best_ids[0], numeric_best_set="|".join(best_ids), best_q_star_m2=best_q,
                  safe_action_count=int(np.sum(qs > 0)), unsafe_action_count=int(np.sum(qs <= 0)))
        for i in range(5):
            for j in range(i+1, 5):
                d = float(qs[i]-qs[j])
                pr = dict(horizon=horizon, context_id=context["context_id"], split=context["split"],
                          action_i=ACTION_IDS[i], action_j=ACTION_IDS[j], q_i_m2=float(qs[i]),
                          q_j_m2=float(qs[j]), signed_difference_m2=d, absolute_difference_m2=abs(d),
                          numeric_tie=bool(abs(d)<=NUMERIC_TOLERANCE))
                for margin in config["thresholds_m2"]:
                    pr[f"separated_gt_{margin:g}"] = bool(abs(d)>margin)
                pairs.append(pr)
        for margin in config["thresholds_m2"]:
            cr[f"informative_gt_{margin:g}"] = bool(spread>margin)
            cr[f"separated_pairs_gt_{margin:g}"] = sum(bool(abs(qs[i]-qs[j])>margin) for i in range(5) for j in range(i+1,5))
        contexts.append(cr)
        for i, (aid, result) in enumerate(zip(ACTION_IDS, evaluated)):
            witnessed_q = float(safety(result["witness_path"], dynamics).min())
            residual = abs(witnessed_q-result["q_star"])
            max_witness_residual = max(max_witness_residual, residual)
            if residual > NUMERIC_TOLERANCE:
                raise AssertionError("Witness mismatch")
            row = dict(horizon=horizon, context_id=context["context_id"], split=context["split"],
                       x0=context["state"][0], y0=context["state"][1], theta0_rad=context["state"][2],
                       action_id=aid, q_star_m2=result["q_star"],
                       support_failure=result["support_failure"], boundary_ambiguous=result["boundary_ambiguous"],
                       robust_regret_m2=best_q-result["q_star"], best_action=best_ids[0],
                       numeric_best_set="|".join(best_ids), spread_m2=spread,
                       witness_id=result["witness_id"], witness_min_time=result["witness_min_time"],
                       witness_delta=json.dumps(result["witness_delta"].tolist(),separators=(",",":")),
                       witness_replay_residual_m2=residual,
                       min_norm_squared=float(np.min(np.sum(result["min_positions"]**2,axis=1))))
            failure_mask = result["branch_min_safety"]<=0
            for p, w in weights.items():
                row[f"failure_probability_p{p:g}"] = float(np.sum(w[failure_mask],dtype=np.float64))
            for margin in config["thresholds_m2"]:
                row[f"near_optimal_within_{margin:g}"] = bool(best_q-result["q_star"]<=margin)
            results.append(row)
            arrays.append(result["branch_min_safety"])
            for t, state in enumerate(result["witness_path"]):
                witnesses.append(dict(horizon=horizon,context_id=context["context_id"],split=context["split"],
                                      action_id=aid,witness_id=result["witness_id"],time_index=t,
                                      x_m=state[0],y_m=state[1],theta_rad=state[2],
                                      safety_C_m2=float(safety(state,dynamics)),danger_margin_m2=-float(safety(state,dynamics)),
                                      outgoing_delta="" if t==horizon else int(result["witness_delta"][t]),
                                      outgoing_action="" if t==horizon else actions[i,t]))
    np.savez_compressed(out/"raw"/f"BRANCH_MINIMA_H{horizon}.npz",
                        branch_min_safety=np.stack(arrays),disturbances=ds,actions=actions,
                        context_ids=np.asarray([c["context_id"] for c in config["contexts"]]),
                        action_ids=np.asarray(ACTION_IDS),
                        row_keys=np.asarray([f"{r['context_id']}:{r['action_id']}" for r in results]),
                        probability_p02=weights[0.2],probability_p04=weights[0.4])
    tests = [r for r in contexts if r["split"]=="test"]
    summary = dict(horizon=horizon, branch_count=1<<horizon, context_count=24,test_count=len(tests),
                   query_count=len(results), branch_query_evaluations=len(results)*(1<<horizon),
                   informative_test_counts={f"{m:g}":sum(r[f"informative_gt_{m:g}"] for r in tests) for m in config["thresholds_m2"]},
                   separated_test_pair_counts={f"{m:g}":sum(r[f"separated_pairs_gt_{m:g}"] for r in tests) for m in config["thresholds_m2"]},
                   numeric_tied_test_pairs=sum(p["numeric_tie"] for p in pairs if p["split"]=="test"),
                   max_witness_replay_error_m2=max_witness_residual,
                   probability_mass={str(p):float(w.sum()) for p,w in weights.items()},
                   test_spread_min_m2=min(r["spread_m2"] for r in tests),
                   test_spread_max_m2=max(r["spread_m2"] for r in tests),
                   test_states_with_safe_and_unsafe_actions=sum(0<r["safe_action_count"]<5 for r in tests),
                   elapsed_seconds=time.perf_counter()-start)
    return results,pairs,contexts,witnesses,summary


def run(config_path, output_dir):
    config_path, out = Path(config_path),Path(output_dir)
    config=json.loads(config_path.read_text(encoding="utf-8"))
    if config != frozen_config():
        raise ValueError("Configuration differs from the frozen design; no search is allowed.")
    (out/"raw").mkdir(parents=True,exist_ok=True)
    started=datetime.now(timezone.utc).isoformat()
    rows,pairs,contexts,witnesses,main_summary=run_horizon(config,12,out)
    summaries=[main_summary]
    fallback=main_summary["informative_test_counts"]["0.005"]<8
    print("H=12:",json.dumps(main_summary,sort_keys=True),flush=True)
    if fallback:
        extra=run_horizon(config,16,out)
        for target, additions in zip([rows,pairs,contexts,witnesses],extra[:4]):target.extend(additions)
        summaries.append(extra[4])
        print("H=16 fallback:",json.dumps(extra[4],sort_keys=True),flush=True)
    else:
        print("H=16 fallback NOT triggered; no H=16 separation experiment was run.",flush=True)
    dump_csv(out/"ACTION_SEPARATION_RESULTS.csv",rows)
    dump_csv(out/"raw"/"PAIRWISE_ACTION_DIFFERENCES.csv",pairs)
    dump_csv(out/"raw"/"CONTEXT_SUMMARY.csv",contexts)
    dump_csv(out/"raw"/"WORST_CASE_WITNESSES.csv",witnesses)
    metadata=dict(started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
                  python=sys.version,executable=sys.executable,numpy=np.__version__,platform=platform.platform(),
                  processor=platform.processor(),config_sha256=sha256_file(config_path),
                  implementation_sha256=sha256_file(__file__),cpu_only=True,
                  torch_imported="torch" in sys.modules,fallback_executed=fallback,summaries=summaries,
                  output_semantics="All 24 frozen contexts retained; inclusive t=0..H and boundary; no model performance measured")
    (out/"raw"/"EXECUTION_METADATA.json").write_text(canonical_json(metadata),encoding="utf-8")
    return metadata


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--freeze-config",type=Path)
    p.add_argument("--config",type=Path)
    p.add_argument("--output-dir",type=Path)
    args=p.parse_args()
    if args.freeze_config:
        with args.freeze_config.open("x",encoding="utf-8") as f:f.write(canonical_json(frozen_config()))
        print("Frozen config:",args.freeze_config,"SHA256",sha256_file(args.freeze_config))
    elif args.config and args.output_dir:
        run(args.config,args.output_dir)
    else:p.error("Use --freeze-config PATH, or --config PATH --output-dir PATH")


if __name__=="__main__":
    main()
