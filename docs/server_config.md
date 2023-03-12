## Nginx

- `/etc/nginx/sites-enabled/demo`

```perl
server {
    listen 80;
    server_name wenshu-demo.dex.moe;

    location / {
        proxy_pass http://localhost:3000; // Change this to the address of your app server
    }
}
```

## SSL/TLS

use [let's encrypt](https://letsencrypt.org/)