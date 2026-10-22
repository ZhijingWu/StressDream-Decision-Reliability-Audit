# Technical note source

Independent technical investigation; unpublished. The two original figures are an experimental-contract TikZ schematic and a chart of retained readout measurements. The chart is not a world-model prediction-error comparison.

Compile from this directory using an existing TeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape Zhijing_Wu_StressDream_Decision_Reliability_Note.tex
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape Zhijing_Wu_StressDream_Decision_Reliability_Note.tex
```

Keep `figures/decision_pipeline.tex` and `figures/readout_error.pdf` at their relative paths. Optional `python -B figures/make_readout_figure.py` redraws saved values only, using existing Matplotlib; it runs no experiment. The empirical p95 values are .007388413463612402 and .00989602124670929 m², n=16 per domain, compared with a .005 m² ranking margin and .00125 m² per-action target.
