# valve-guardian-web

A server-rendered page that uploads cycles, asks the API, and draws the
verdicts. It is a client of the API like any other: it imports the contract,
never the model.

```mermaid
%%{init: {"flowchart": {"rankSpacing": 40}}}%%
graph LR
    browser([browser])
    subgraph web ["`**Frontend**: valve-guardian-web`"]
        subgraph pages [pages/]
            routes["routes: /, /analyses,<br/>Jinja templates"]
            figures["figures/: the SVG<br/>charts routes draw"]
        end
        subgraph analysis [analysis/]
            signals["UploadedSignals: parse"]
            store["AnalysisStore: last 3"]
        end
        subgraph api_client [api/]
            client["ApiClient: 64 per batch"]
        end
    end
    api([api])
    contract["valve-guardian-contract:<br/>PredictionRequest, Response"]
    browser ~~~ figures
    browser -->|PS2.txt, FS1.txt| routes
    routes -->|parse| signals
    routes -->|keep| store
    routes -->|signals| client
    client -->|HTTP| api
    client -.- contract
    classDef module fill:#2f6f8f,stroke:#1d4a60,color:#ffffff
    classDef library fill:#00838f,stroke:#005662,color:#fff,stroke-dasharray:5
    classDef external fill:#616161,stroke:#424242,color:#ffffff
    class routes,figures,signals,store,client module
    class contract library
    class browser,api external
    style web fill:none,stroke:#f9a825,stroke-width:3px
    style pages fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style analysis fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
    style api_client fill:none,stroke:#9e9e9e,stroke-dasharray:4 3
```

A solid arrow runs on every upload; a dotted line without a head imports
the types of another library.

The API caps a request at 256 cycles; the client sends 64 at a time and
joins the answers, so a whole recording of 2205 cycles goes through.

The store keeps the last three analyses in memory: a restart, or a fourth
upload, sends the oldest link to a 404 that asks for the files again.

`VALVE_GUARDIAN_WEB_API_URL` says where the API answers; it has no default.
Run it with `just web`, or build it with `just image::build web`.
