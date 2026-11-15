# valve-guardian-web

A server-rendered page that uploads cycles, asks the API, and draws the
verdicts. It is a client of the API like any other: it imports the contract,
never the model.

`VALVE_GUARDIAN_WEB_API_URL` says where the API answers; it has no default.
Run it with `just web`, or build it with `just image::build web`.
