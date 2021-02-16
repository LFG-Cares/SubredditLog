# HTTP Server Setup

This documentation provides example configurations for [nginx](https://www.nginx.com/resources/wiki/). While
any HTTP server with supports WSGI should be compatible, only nginx is supported.

!!! info
    For the sake of brevity, only Ubuntu 20.04 instructions are provided here. These tasks are not unique to SubredditLog and should carry over to other distributions with minimal changes. Please consult your distribution's documentation for assistance if needed.

## Obtain an SSL Certificate

To enable secure, HTTPS access to SubredditLog, an SSL certificate is required. We recommend obtaining one from
[Let's Encrypt](https://letsencrypt.org/getting-started/). Both the public certificate and private key files are needed.

## HTTP Server Installation

Begin by installing nginx:

```shell
sudo apt install -y nginx
```

Once installed, copy the following configuration into a new file called `/etc/nginx/sites-available/subredditlog`. Be 
sure to replace `subredditlog.example.com` with the domain name or IP address of your new installation. (This should 
also match the value configured for `ALLOWED_HOSTS` in `env.config`.) 

You'll also need to change the `ssl_certificate` and `ssl_certificate_key` lines to match the locations of your public 
certificate and private key files.

```
server {
    listen 443 ssl;

    # CHANGE THIS TO YOUR SERVER'S NAME
    server_name subredditlog.example.com;

    # CHANGE THESE TO MATCH THE LOCATIONS OF YOUR CERTIFICATE AND PRIVATE KEY
    ssl_certificate /etc/letsencrypt/live/subredditlog.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/subredditlog.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:7654;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    # Redirect HTTP traffic to HTTPS
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}
```

Then, delete `/etc/nginx/sites-enabled/default` and create a symlink in the `sites-enabled` directory to the 
configuration file you just created.

```shell
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/subredditlog /etc/nginx/sites-enabled/subredditlog
```

Finally, restart the `nginx` service to use the new configuration.

```shell
sudo systemctl restart nginx
```

## Confirm Connectivity

At this point, you should be able to connect to the HTTPS service at the server name or IP address you provided.

!!! info
    Please keep in mind that the configurations provided here are bare minimums required to get SubredditLog up and running. You may want to make adjustments to better suit your production environment.

## Troubleshooting

If you are unable to connect to the HTTP server, check that:

* Nginx/Apache is running and configured to listen on the correct port.
* Access is not being blocked by a firewall somewhere along the path. (Try connecting locally from the server itself.)

If you are able to connect but receive a 502 (bad gateway) error, check the following:

* The docker-compose stack is up and running.
* SELinux is not preventing the reverse proxy connection. You may need to allow HTTP network connections with the 
  command `setsebool -P httpd_can_network_connect 1`
