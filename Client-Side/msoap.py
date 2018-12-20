from suds.client import Client as SudsClient
from suds import MethodNotFound
from threading import Thread
from threading import Lock
from suds import WebFault
from functools import partial
import random
import sys
import urllib2
from datetime import datetime

instance_lock = Lock();
successes = 0;

def call_once(results, function, arguments, address, index, rid):
    '''Call a SOAP request once and return its output to the provided list.

    Parameters
    ----------
    results : list
        A list of results where the output of this function will be returned.
    function : string
        The name of the function that is wished to be called on each of the 
        servers.
    arguments : list
        This can be None, but should be some list.
    address : string
        The address and port of the SOAP service.
    index : int
        The index of the input.
    successes : int
        The number of successes to be sent to the server.
    rid : int
        The request id of the request.
    
    Returns
    -------
    None
    '''
    global successes
    url = 'http://%s/soap/someservice?wsdl' % address
    try:
        client = SudsClient(url=url, cache=None)
        #if result(*args) is not error, set return value to return.
        method = getattr(client.service, function)
        if arguments is None:
            instance_lock.acquire()
            args = [rid, successes]
            successes += 1
            instance_lock.release()
        else:
            instance_lock.acquire()
            args = arguments + [rid,successes]
            successes += 1
            instance_lock.release()
            
        results[index] = method(*args)
        
        
    except urllib2.URLError:
        results[index] = None
    except MethodNotFound:
        results[index] = None
    except WebFault:
        results[index] = None
    

def multicast(servers, function, arguments=None):
    '''Send SOAP requests to all the servers provided, and assume our system
    is properly configured.

    Parameters
    ----------
    servers : list
        A list of strings that denote the name and port of each service.  It is 
        important that these are denoted as [name]:[port], as they will be used
        as such later.
    function : string
        The name of the function that is wished to be called on each of the 
        servers.
    arguments : list, optional
        This can be left blank, but should be some list.

    Returns
    -------
    unknown : output
        This will return the output from the function.

    Raises
    ------
    suds.MethodNotFound
        Raised if no service can handle the function called.
    TypeError
        Improper types used.
    '''
    global successes;
    
    #data validation
    if False:
        raise TypeError("Improper type.");
    
    threads = [None] * len(servers)
    results = [None] * len(servers)
    
    successes = 0;
    random.seed(datetime.now())
    rid = random.randint(0,sys.maxint)
    
    for i in range(len(threads)):
        threads[i] = Thread(target=call_once, args=(results, function, 
                                                    arguments, servers[i], i, 
                                                    rid))
        threads[i].start()
    
    for i in range(len(threads)):
        threads[i].join()
    
    output = None
    
    #get the only valid result
    for result in results:
        if result is not None:
            if output is None:
                output = result
            else:
                raise EnvironmentError("Environment is not configured properly.")
    
    #if none are valid, let's raise an error.
    if output is None:
        raise MethodNotFound("Method not found in environment.")
    else:
        return output