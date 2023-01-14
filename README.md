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

# Add modules

Copy and adjust : 

Add the API function :

```
async def handler_ss(request):

    raw = os.popen("ss -ptnaH").readlines()
    ret = []
    for line in raw :

        tab = line.strip().split()
        ret.append({
            "state" : tab[0],
            "local_addr" : tab[3].split(':')[0],
            "local_port" : tab[3].split(':')[1],
            "remote_addr" : tab[4].split(':')[0],
            "remote_port" : tab[4].split(':')[1],
            "proc" : " ".join(tab[5:])[:120]

        })
    return web.json_response(text=json.dumps(ret))

```

Add and adjust the corresponding html part :

```
       <h1 id="ss">Network connections</h1>
        <table  x-data=" { conns : [] } " x-init="fetch('/systemapi/ss')
        .then(response => response.json())
        .then(data => conns = data)" class="uk-table uk-table-striped">
            <thead>
                <tr>
                    <th>Connections State</th>
                    <th>Local addr</th>
                    <th>Local port</th>
                    <th>Remote addr</th>
                    <th>Remote port</th>
                    <th>Process</th>
                    
                </tr>
            </thead>
            <tbody>
            <template x-for="p in conns">
                <tr>
                    <td x-text="p.state"></td>
                    <td x-text="p.local_addr"></td>
                    <td x-text="p.local_port"></td>
                    <td x-text="p.remote_addr"></td>
                    <td x-text="p.remote_port"></td>
                    <td x-text="p.proc"></td>
                </tr>
            </template>
            </tbody>
        </table>
```
