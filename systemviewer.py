import time
import secrets
from aiohttp import web
import os
import json

async def handler_process(request):

    name = 'pid'
    tri = '+'

    try:
        name = request.rel_url.query['name']
        tri = request.rel_url.query['tri']

        if name not in ["user","pid","ppid","pcpu","pmem","start","cmd"]:
            name = "pid"
        tri = '-' if request.rel_url.query['tri'] == 'false' else '+'
    except:
        pass

    raw = os.popen(f"ps x -o user,pid,ppid,pcpu,pmem,start,cmd --ppid 2 -p 2 --deselect --sort {tri}{name}").readlines()
    ret = []
    for line in raw[1:] :

        tab = line.strip().split()
        ret.append({
            "user" : tab[0],
            "pid" : tab[1],
            "ppid" : tab[2],
            "pcpu" : tab[3],
            "pmem" : tab[4],
            "start" : tab[5],
            "cmd" : " ".join(tab[6:])[:120]
        })
    return web.json_response(text=json.dumps(ret))

async def handler_hd(request):

    raw = os.popen("df -hPT").readlines()
    ret = []
    for line in raw[1:] :
        tab = line.strip().split()
        ret.append({
            "fs" : tab[0],
            "type" : tab[1],
            "size" : tab[2],
            "used" : tab[3],
            "avail" : tab[4],
            "pused" : tab[5],
            "mount" : tab[6]
        })
    return web.json_response(text=json.dumps(ret))

async def handler_net(request):

    raw = os.popen("ip -br a").readlines()
    ret = []
    for line in raw[1:] :

        tab = line.strip().split()
        ret.append({
            "iface" : tab[0],
            "state" : tab[1],
            "addr" : " ; ".join(tab[2:])
        })
    return web.json_response(text=json.dumps(ret))

async def handler_info(request):

    cmd = {
        "date" : "date",
        "uname"  : "uname -a",
        "uptime" : "uptime",
        "hostname" : "hostname",
    }
    ret = [ {'key' : k, 'value': os.popen(v).read().strip()} for k,v in cmd.items()]
    return web.json_response(text=json.dumps(ret))

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

async def handler_f2b(request):

    raw = os.popen("tail -n 100 /var/log/fail2ban.log").readlines()
    ret = []
    for line in raw :
        tab = line.strip().split()
        ret.append({
            "date" : " ".join(tab[0:2]),
            "level" : tab[3],
            "details" : " ".join(tab[4:])[:120]
        })
    return web.json_response(text=json.dumps(ret))

def init():
    app = web.Application()
#   app.router.add_route('GET', '/systemapi/service/{name}/{action}', handler)
#   app.router.add_route('GET', '/systemapi/service/logs', handler)
    app.router.add_route('GET', '/systemapi/processes', handler_process)
    app.router.add_route('GET', '/systemapi/net', handler_net)
    app.router.add_route('GET', '/systemapi/ss', handler_ss)
    app.router.add_route('GET', '/systemapi/info', handler_info)
    app.router.add_route('GET', '/systemapi/hdresources', handler_hd)
    app.router.add_route('GET', '/systemapi/f2b', handler_f2b)
    return app

web.run_app(init(), host="127.0.0.1", port=4500)
