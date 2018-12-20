from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from time import strftime
from hlsi import HyperLedgerSoapInteractive as hlSOAPi
from spyne.error import Fault
import netifaces as ni
import socket

app = Flask(__name__)
spyne = Spyne(app)

#basic configuration
host_ip = ""; #this needs to be configured manually.
hlsi = None;

class SomeSoapService(spyne.Service):
    __service_url_path__ = '/soap/someservice'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
    
    @spyne.rpc(Integer, Integer, _returns=str)
    def get_time(ctx, rid,successes):
        #verify
	if not hlsi.verify("get_time",rid,successes,ctx.transport.req["REMOTE_ADDR"]):
            #if we shouldn't be servicing this request, return an error value.
	    raise Fault(faultcode="Server Unwilling", faultstring="Here's your error.");
        else:
            #if we should, return our value.
	    return strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    @spyne.rpc(Unicode, Integer, Integer, Integer, _returns=Iterable(Unicode))
    def echo(ctx, strin, cnt, rid, successes):
        #verify
        if not hlsi.verify("echo",rid,successes,ctx.transport.req["REMOTE_ADDR"]):
            #if we shouldn't be servicing this request, return an error value.
            raise Fault(faultcode="Server Unwilling", faultstring="Here's your error.");
        else:
            for i in range(cnt):
                yield strin
    
    @spyne.rpc(Integer,Integer,Integer,Integer,_returns=Integer)
    def add_ints(ctx, x,y,rid,successes):
        #verify
        if not hlsi.verify("add_ints",rid,successes,ctx.transport.req["REMOTE_ADDR"]):
            #if we shouldn't be servicing this request, return an error value.
            raise Fault(faultcode="Server Unwilling", faultstring="Here's your error.");
        else:
            return x+y

if __name__ == '__main__':
    ni.ifaddresses('eth0')
    host_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    
    #take bash-style input from user
    user_input = raw_input("Run on IP Address [%s]:"%host_ip);
    
    if user_input != "":
        host_ip = user_input;
    
    
    try:
        hlsi = hlSOAPi(host_ip);
        app.run(host = host_ip);
    except socket.gaierror:
        print("Invalid host name.");
