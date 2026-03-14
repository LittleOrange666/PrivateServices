#!/usr/bin/env bash

if [ -f .env ]; then
  echo "File .env already exists. Exiting."
  exit 1
fi

mkdir data
mkdir data/backend
mkdir data/nginx
touch data/nginx/nginx.conf
touch data/nginx/default.conf

RANDOM_PASSWORD=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-32)

cat <<EOF > .env
# Auto-generated on $(date)
ROOT_PASSWORD=$RANDOM_PASSWORD
EOF

echo "🔑 Root Password: $RANDOM_PASSWORD"

docker-compose up -d