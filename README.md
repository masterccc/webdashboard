# webdashboard

Web-based system monitoring.


## Screenshot

![Alt text](https://github.com/masterccc/webdashboard/blob/e135ed2156580f9e0b345871aec3af6b88e88083/dashboardsample.png "Optional title")

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
