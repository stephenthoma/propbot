#gcloud functions deploy gov-bot --runtime python39 --trigger-topic=gov-bot-cron --entry-point main
gcloud functions deploy gov-bot-hook --runtime python39 --trigger-http --allow-unauthenticated --entry-point webhook_entry
