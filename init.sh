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

RANDOM_PASSWORD1=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-32)
RANDOM_PASSWORD2=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-32)

cat <<EOF > .env
# Auto-generated on $(date)
ROOT_PASSWORD=$RANDOM_PASSWORD1
SECRET_KEY=$RANDOM_PASSWORD2
EOF

echo "🔑 Root Password: $RANDOM_PASSWORD1"

docker-compose up -d