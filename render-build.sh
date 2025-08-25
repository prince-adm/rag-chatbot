#!/usr/bin/env bash
# exit on error
set -o errexit

# Create and activate a swapfile
fallocate -l 1G /swapfile
mkswap /swapfile
swapon /swapfile

# Install dependencies
pip install -r requirements.txt

# Run the indexer
python indexer.py