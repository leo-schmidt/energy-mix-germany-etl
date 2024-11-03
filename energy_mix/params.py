import os

# Azure
STORAGE_ACCOUNT = os.environ.get("STORAGE_ACCOUNT")
CONTAINER = "energymix"
RAW_PATH = "smard-data-raw"
MERGED_PATH = "smard-data-merged"

# Smard
REGION = "DE"
RESOLUTION = "HOUR"
