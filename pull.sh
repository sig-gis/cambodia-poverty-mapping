#!/bin/bash
git reset --hard HEAD
git pull
# cd povertymappingapp
rm -r static/
python3 manage.py collectstatic
sudo systemctl restart gunicorn.socket
sudo systemctl restart nginx
