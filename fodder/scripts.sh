# get-graphql-schema https://hub.snapshot.org/graphql --json > snapshot_schema.json
#
# sgqlc-codegen schema snapshot_schema.json govbot/snapshot_schema.py
#
# # gcloud scheduler jobs create pubsub gov-bot-summary \
#    --schedule="0 0 * * mon" --topic="gov-bot-cron" \
#    --message-body="summary"
#
# gcloud scheduler jobs create pubsub gov-bot \
#    --schedule="*/15 * * * *" --topic="gov-bot-cron" \
#    --message-body="check_special"


