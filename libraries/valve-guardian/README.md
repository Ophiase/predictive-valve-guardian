# valve-guardian

The features and the inference: what the API needs, and nothing more.

- [`features/`](src/valve_guardian/features): per-cycle statistics, their
  differences and the Fourier magnitudes, in NumPy.
- [`inference/`](src/valve_guardian/inference): loads the model card,
  rebuilds the features it names, runs the ONNX model.
- [`artifact/`](src/valve_guardian/artifact): the deployed `model.onnx` and
  its `model-card.json`, written by `just train`.

It depends on NumPy, ONNX Runtime and the contract.
