if [ "$1" == "dev" ]; then
    CONF_FILENAME="dev.yaml"
elif [ "$1" == "prod" ]; then
    CONF_FILENAME="prod.yaml"
else
    echo "Must pass <dev | prod>"
    exit 1
fi

# Unset all env variables
sed -e 's/^/unset /g;s/:.*$//g' prod.yaml

# Export env variables for chosen config
sed -e 's/^/export /g;s/:[^:\/\/]/="/g;s/$/"/g;s/ *=/=/g' $CONF_FILENAME
