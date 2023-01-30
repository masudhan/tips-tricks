```

sudo add-apt-repository ppa:certbot/certbot
sudo apt install -y nginx python-certbot-nginx

vi /etc/nginx/sites-available/default

# replace test
 upstream test {
  server 127.0.0.1:3000 fail_timeout=0;
}

server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
        # replace test
        server_name test.ch-ms.co.in;

        location / {
                proxy_set_header        Host $host:$server_port;
                proxy_set_header        X-Real-IP $remote_addr;
                proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header        X-Forwarded-Proto $scheme; 
                proxy_set_header        Upgrade $http_upgrade;
                proxy_set_header        Connection "upgrade";
                proxy_pass              http://test; # replace test
        }
}

sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d test.ch-ms.co.in

```
