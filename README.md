# propbot
This repo contains the code used to power [@proposalbot](https://twitter.com/proposalbot).

The bot is operated by two cloud functions with entrypoints in the `main.py` file. Both functions can be created using the `deploy.sh` script.
- gov-bot-hook: An HTTP triggered function that runs every time a proposal is created
- gov-bot-cron: A pub-sub triggered function that is run on a schedule by a scheduler job

The bot currently tweets about new proposals, high activity proposals, and contested proposals.
Refer to the specified filters in `main.py` for each tweet type (as well as their implementations in `proposal_filters.py`)

An auto-generated SGQLC schema (`snapshot_schema.py`) is used for interaction with the Snapshot GraphQL API.
Supporting API queries are implemented in the `snapshot.py` file.
