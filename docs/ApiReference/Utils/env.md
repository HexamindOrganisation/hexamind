# Env Template

## Overview

The library provided also a utils to automatically generate a .env.template file to configure your project.

## How to use it 

```bash

hxmrag-env --destination /path/to/destination/folder/for/env/ 

```

## Env file

This is what the template env file will look like:

```env

#.env.template
# This file contains the environment variables that are used by the application.
# You should copy this file to .env and fill in the values for your environment.
# The hexsrag-env command will copy the .env for you. 

# Database
DATABASE_PATH=path/to/database
COLLECTION_NAME=collection_name
DB_NAME=db_name

#API_DB_NAME = api_db_name
#API_DB_HOST = api_db_host
#API_DB_PORT = api_db_port
#API_DB_USER = api_db_user
#API_DB_PASSWORD = api_db_password
#ES_CLOUD_ID = es_cloud_id
#ES_API_KEY = es_api_key
#ES_CA_CERT = es_ca_cert
#ES_SSL_ASSERT = es_ssl_assert

# LLM
LLM_NAME=llm_name
LLM_API_KEY=llm_api_key
#LLM_MODEL=llm_model # e.g. "gpt-3.5-turbo" or "mistral-large-latest" this name is linked to the LLM_NAME and LLM_API_KEY (not a mandatory variable)
#LLM_EMBED_MODEL=llm_embed_model # e.g. "text-embedding-3-large" or "mistral-embed" this name is linked to the LLM_NAME and LLM_API_KEY (not a mandatory variable)

```