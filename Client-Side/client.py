from suds.client import Client as SudsClient
from suds import MethodNotFound
from suds import WebFault
from msoap import multicast
import time
from threading import Thread

iteration = 0;
while iteration < 4:
    start = time.time()
    try:
        servers = ['3.83.66.65:5000','54.175.172.25:5000']
        ordered_servers = [];
        ordered_servers.append(servers[int(start)%2]);
        ordered_servers.append(servers[int(start+1)%2]);
        multicast(ordered_servers,"get_time")
    except MethodNotFound:
        print("");
    print(str(time.time()-start)) #get client latency
    iteration += 1;