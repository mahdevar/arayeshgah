#!/bin/bash
git pull
docker compose up --detach --force-recreate app
