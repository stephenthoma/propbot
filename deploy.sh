gcloud functions deploy gov-bot-cron \
    --runtime python39 --trigger-topic=gov-bot-cron \
    --entry-point cron_entry --env-vars-file ./config/prod.yaml 

gcloud functions deploy gov-bot-hook \
    --runtime python39 --trigger-http \
    --allow-unauthenticated --entry-point webhook_entry \
    --env-vars-file ./config/prod.yaml 
