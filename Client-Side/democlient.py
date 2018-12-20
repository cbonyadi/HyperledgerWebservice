from suds.client import Client as SudsClient
from suds import MethodNotFound
from suds import WebFault
from msoap import multicast
import time
from threading import Thread

servers = ['54.175.172.25:5000','3.83.66.65:5000']

start_1 = time.time()
try:
    print(multicast(servers,"get_time"));
except MethodNotFound:
    print("Err testing get_time.");
print(str(time.time()-start_1)) #get client latency

start_2 = time.time()
try:
    print(multicast(servers,"add_ints",[1,2]));
except MethodNotFound:
    print("Err testing add_ints.");
print(str(time.time()-start_2)) #get client latency