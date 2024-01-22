#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# install nginx
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update && sudo apt-get -y install nginx
fi
# create folders
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
sudo sh -c 'echo "Hello world" > /data/web_static/releases/test/index.html'
# create a symblic link and give ownership
if [ -L "/data/web_static/current" ]; then
    sudo rm -r /data/web_static/current
fi
sudo ln -sf /data/web_static/current /data/web_static/releases/test
sudo chown -R ubuntu:ubuntu /data/
#
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html;

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
    
    location / {
      add_header X-Served-By "$(hostname)";
      try_files \$uri \$uri/ =404;
   }

   location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
   }
}
EOF
sudo service nginx restart
