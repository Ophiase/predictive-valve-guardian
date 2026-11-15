# valve-guardian-training

Everything offline: the only place scikit-learn, XGBoost and MLflow live.

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
