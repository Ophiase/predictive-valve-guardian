# valve-guardian-api

A FastAPI service over the deployed model; OpenAPI at `/docs`.

| Route | Answer |
| --- | --- |
| `POST /predictions` | one verdict and probability per cycle |
| `GET /model` | the model card |
| `GET /health` | `{"status": "ok"}` |

Settings come from `VALVE_GUARDIAN_API_*`: `HOST`, `PORT`,
`MODEL_DIRECTORY`. Run it with `just api`, or build it with
`just image::build api`.
