# valve-guardian-training

Everything offline: the only place scikit-learn, XGBoost and MLflow live.

```mermaid
%%{init: {"flowchart": {"rankSpacing": 40}}}%%
graph LR
    subgraph training ["`**Training**: valve-guardian-training`"]
        subgraph dataset [dataset/]
            cycles["Cycles: 2205,<br/>UCI archive"]
        end
        subgraph workflows [workflows/]
            benchmark["Benchmark:<br/>3 models x 7<br/>representations"]
        end
        subgraph evaluation [evaluation/]
            evaluate["CrossValidation: 5 x 3<br/>Selection<br/>Holdout: last 205"]
        end
        subgraph estimators [estimators/]
            export["OnnxExport:<br/>parity"]
        end
    end
    report[("docs/benchmark.md")]
    artifact["valve-guardian:<br/>artifact/"]
    cycles --> benchmark --> evaluate --> export
    benchmark --> report
    export -->|just train| artifact
    classDef module fill:#2f6f8f,stroke:#1d4a60,color:#ffffff
    classDef library fill:#00838f,stroke:#005662,color:#fff,stroke-dasharray:5
    classDef file fill:#b8732a,stroke:#7f4e1a,color:#ffffff
    class cycles,benchmark,evaluate,export module
    class artifact library
    class report file
    style training fill:none,stroke:#f9a825,stroke-width:3px
    style dataset fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style workflows fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style evaluation fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style estimators fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
```

The two evaluations answer different questions: shuffled folds pick the
model, the chronological holdout tells whether it survives the drift of the
last cycles. The card records both. `Trainer` runs the chain, and
`tracking/` keeps the run in `runs/`, or in MLflow when it is set.

- [`dataset/`](src/valve_guardian_training/dataset): downloads and
  fingerprints the UCI dataset, splits it in recording order.
- [`estimators/`](src/valve_guardian_training/estimators): the candidates
  and the ONNX export with its parity check.
- [`evaluation/`](src/valve_guardian_training/evaluation): repeated
  stratified cross-validation, the holdout, the selection.
- [`tracking/`](src/valve_guardian_training/tracking): a local tracker, and
  an MLflow one behind the optional `mlflow` extra.
- [`workflows/`](src/valve_guardian_training/workflows): `benchmark` and
  `train`, the command line `valve-guardian-training`.
