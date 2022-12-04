#!/bin/bash

ROOT="/workspaces/omega-triage-portal"

# Create and activate the virtual environment
echo "Creating virtual environment."
python -mvenv .venv
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python (back-end) dependencies."
cd $ROOT/src
python -m pip install --upgrade pip
pip install wheel
pip install -r ./requirements.txt

# Install JavaScript dependencies
echo "Installing JavaScript (front-end) dependencies."
cd $ROOT/src
npm i -g yarn
yarn

# Update default environment
echo "Creating development environment."
cd $ROOT/src
cp .env-template .env
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(64))")
sed -i "s/%RANDOM_STRING%/$SECRET_KEY/" .env
unset SECRET_KEY

# Create working directories
echo "Creating working directories."
mkdir $ROOT/logs

# Set up database
echo "Setting up datatbase."
cd $ROOT/src
python manage.py migrate
python manage.py makemigrations
python manage.py migrate triage

# Create superuser
DJANGO_SUPERUSER_USERNAME="admin" \
DJANGO_SUPERUSER_PASSWORD="admin" \
DJANGO_SUPERUSER_EMAIL="nobody@localhost" \
python manage.py createsuperuser --noinput

echo "Initialization completed."
