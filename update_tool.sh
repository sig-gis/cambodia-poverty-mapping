#!/bin/bash
git reset --hard HEAD
git pull
cd /home/nis-mop/cambodia-poverty-mapping
python3 manage.py collectstatic
# sudo systemctl restart gunicorn.socket
# sudo systemctl restart nginx
sudo docker stop cambodia-poverty-mapping-web-1
sudo docker rm cambodia-poverty-mapping-web-1
sudo docker compose build
sudo docker compose up -d