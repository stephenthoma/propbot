gcloud functions deploy gov-bot-cron \
    --runtime python39 --trigger-topic=gov-bot-cron \
    --entry-point cron_entry --env-vars-file ./config/prod.yaml 

gcloud functions deploy gov-bot-hook \
    --runtime python39 --trigger-http \
    --allow-unauthenticated --entry-point webhook_entry \
    --env-vars-file ./config/prod.yaml 


# gcloud scheduler jobs create pubsub gov-bot-summary \
#    --schedule="0 0 * * mon" --topic="gov-bot-cron" \
#    --message-body="summary"

# gcloud scheduler jobs create pubsub gov-bot \
#    --schedule="*/15 * * * *" --topic="gov-bot-cron" \
#    --message-body="check_special"
