# valve-guardian-contract

The pydantic models every side agrees on: the API serves them, the page
sends them, the training writes them.

```mermaid
%%{init: {"flowchart": {"rankSpacing": 40}}}%%
graph TD
    training([training])
    api([api])
    web([web])
    subgraph contract ["`**Contract**: valve-guardian-contract`"]
        subgraph card [card/]
            model_card[ModelCard]
            feature_settings[FeatureSettings]
            metric_summary[MetricSummary]
        end
        subgraph prediction [prediction/]
            request[PredictionRequest]
            response[PredictionResponse]
            cycle["Cycle: 6000 PS2, 600 FS1"]
            verdict["Prediction: optimal, p"]
        end
    end
    training -.-|writes| model_card
    api -.-|serves| model_card
    api -.-|answers| response
    web -.-|sends| request
    model_card --> feature_settings
    model_card -->|per metric| metric_summary
    request -->|1 to 256| cycle
    response -->|one per cycle| verdict
    classDef module fill:#2f6f8f,stroke:#1d4a60,color:#ffffff
    classDef library fill:#00838f,stroke:#005662,color:#fff,stroke-dasharray:5
    classDef external fill:#616161,stroke:#424242,color:#ffffff
    classDef file fill:#b8732a,stroke:#7f4e1a,color:#ffffff
    class model_card,feature_settings,metric_summary module
    class request,response,cycle,verdict module
    class training,api,web external
    style contract fill:none,stroke:#f9a825,stroke-width:3px
    style card fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style prediction fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
```

A dotted line is a side that imports the model; a solid arrow is a model
that holds another.

No side owns a model: a field changes here, and every side sees it at once.

- [`Cycle`](src/valve_guardian_contract/prediction/cycle.py): one cycle, 6000 pressure
  and 600 flow samples, checked on arrival.
- [`PredictionRequest`, `PredictionResponse`](src/valve_guardian_contract/prediction/request.py):
  up to 256 cycles in, one verdict and one probability per cycle out.
- [`ModelCard`](src/valve_guardian_contract/card/model_card.py): the features,
  the metrics, the dataset hash and the versions of a trained model.

It depends on pydantic only.
