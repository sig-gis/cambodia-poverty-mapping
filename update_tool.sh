#!/bin/bash
cd /home/nis-mop/cambodia-poverty-mapping
git pull
sudo docker stop cambodia-poverty-mapping-web-1
sudo docker rm cambodia-poverty-mapping-web-1
sudo docker compose build
sudo docker compose up -d