#!/bin/bash

ENV=$1
COMMAND=${2:-up}

if [ -z "$ENV" ]; then
    echo "Usage: ./deploy.sh <env> [command]"
    echo "env: dev, staging, prod"
    echo "command: up, down, build (default: up)"
    exit 1
fi

case $ENV in
    dev|staging|prod)
        docker compose -f docker-compose.base.yml -f docker-compose.$ENV.yml $COMMAND
        ;;
    *)
        echo "Invalid environment. Use dev, staging, or prod"
        exit 1
        ;;
esac