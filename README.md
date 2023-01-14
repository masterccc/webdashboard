# webdashboard

Web-based system monitoring.


## Screenshot

![Alt text](https://raw.githubusercontent.com/masterccc/webdashboard/main/dashboardsample.png "Optional title")

# Nginx config

```
    location /system/ {
        auth_request /auth;
        alias /var/www/dashboard_html/system/;
    }
    location /systemapi {
        auth_request /auth;
        proxy_pass http://127.0.0.1:4500;
    }
```
