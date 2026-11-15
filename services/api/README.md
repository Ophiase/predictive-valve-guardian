# valve-guardian-api

A FastAPI service over the deployed model; OpenAPI at `/docs`.

```mermaid
%%{init: {"flowchart": {"rankSpacing": 40}}}%%
graph LR
    client(["web, curl,<br/>any client"])
    subgraph api ["`**API**: valve-guardian-api`"]
        routes["routes: /predictions,<br/>/model, /health"]
        application["application, settings:<br/>VALVE_GUARDIAN_API_*"]
    end
    contract["valve-guardian-contract:<br/>PredictionRequest, Response"]
    subgraph core ["`**Core**: valve-guardian`"]
        predictor["inference/: Predictor"]
        model[("artifact/: model.onnx<br/>+ model-card.json")]
    end
    client ~~~ application
    client -->|HTTP| routes
    routes -.- contract
    routes -->|PS2, FS1| predictor
    application -.->|loads at start| predictor
    predictor -.->|reads| model
    classDef module fill:#2f6f8f,stroke:#1d4a60,color:#ffffff
    classDef library fill:#00838f,stroke:#005662,color:#fff,stroke-dasharray:5
    classDef external fill:#616161,stroke:#424242,color:#ffffff
    class application,routes module
    class predictor,contract library
    class client external
    classDef file fill:#b8732a,stroke:#7f4e1a,color:#ffffff
    class model file
    style api fill:none,stroke:#f9a825,stroke-width:3px
    style core fill:none,stroke:#005662,stroke-dasharray:4 3
```

A solid arrow runs on every request, a dotted one once at start; a dotted
line without a head imports the types of another library.

No scikit-learn, XGBoost or MLflow here: the model reaches the API as ONNX,
and its card says which features to rebuild.

| Route | Answer |
| --- | --- |
| `POST /predictions` | one verdict and probability per cycle |
| `GET /model` | the model card |
| `GET /health` | `{"status": "ok"}` |

Settings come from `VALVE_GUARDIAN_API_*`: `HOST`, `PORT`,
`MODEL_DIRECTORY`. Run it with `just api`, or build it with
`just image::build api`.
