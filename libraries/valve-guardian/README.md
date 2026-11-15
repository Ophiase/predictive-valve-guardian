# valve-guardian

The features and the inference: what the API needs, and nothing more.

```mermaid
%%{init: {"flowchart": {"rankSpacing": 40}}}%%
graph LR
    api([api])
    subgraph core ["`**Core**: valve-guardian`"]
        subgraph inference [inference/]
            predictor[Predictor]
            model_artifact[ModelArtifact]
            classifier[OnnxClassifier]
        end
        subgraph artifact [artifact/]
            card[("model-card.json")]
            onnx[("model.onnx")]
        end
        subgraph features [features/]
            specification[FeatureSpecification]
            statistics["CycleStatistics: 7 columns"]
            spectrum["spectrum: k FFT magnitudes"]
        end
    end
    contract["valve-guardian-contract:<br/>ModelCard, Prediction"]
    runtime[ONNX Runtime, CPU]
    api -->|PS2, FS1| predictor
    contract -.- predictor
    predictor -.->|at start| model_artifact
    model_artifact -.-> card
    model_artifact -.-> onnx
    predictor -->|1. signals| specification
    specification --> statistics
    specification --> spectrum
    predictor -->|2. feature matrix| classifier
    runtime -..- classifier
    classDef module fill:#2f6f8f,stroke:#1d4a60,color:#ffffff
    classDef library fill:#00838f,stroke:#005662,color:#fff,stroke-dasharray:5
    classDef external fill:#616161,stroke:#424242,color:#ffffff
    classDef file fill:#b8732a,stroke:#7f4e1a,color:#ffffff
    class predictor,model_artifact,classifier module
    class specification,statistics,spectrum module
    class card,onnx file
    class contract library
    class api,runtime external
    style core fill:none,stroke:#f9a825,stroke-width:3px
    style inference fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style artifact fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style features fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
```

A solid arrow runs on every request, a dotted one once at start; a dotted
line without a head imports the types of another library.

The card names the features, so the API rebuilds exactly those the model was
trained on. Per signal, the deployed card asks for:

The deployed model uses order 0 and k = 20: 27 columns per signal, 54 in all.

- [`features/`](src/valve_guardian/features): per-cycle statistics, their
  differences and the Fourier magnitudes, in NumPy.
- [`inference/`](src/valve_guardian/inference): loads the model card,
  rebuilds the features it names, runs the ONNX model.
- [`artifact/`](src/valve_guardian/artifact): the deployed `model.onnx` and
  its `model-card.json`, written by `just train`.

It depends on NumPy, ONNX Runtime and the contract.
