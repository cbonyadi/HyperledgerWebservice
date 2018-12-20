import time

#THIS IS A CLASS
class HyperLedgerSoapInteractive:
    hyperledger = None;
    _ip = "";
    
    #init???
    def __init__(self, ip):
        hyperledger = None;
        self._ip = ip;
    
    
    #function for checking if our service should be run locally, takes function name.
    def verify(self, function, rid, server_instance, ip):
        '''Verify that I should be the one servicing the request by interacting 
        with the hyperledger framework.
    
        Parameters
        ----------
        function : string
            The name of the function that is wished to be called on each of the 
            servers.
        rid : int
            A decently random he request at the behest of the client.
        server_instance : int
            The number of successful calls before this server was called. 
        ip : str
            The client IP.
        
        Returns
        -------
        Bool
            Whether or not this server will be servicing this request
        '''
	print(server_instance);
	time.sleep(10);
        #for the sake of demonstration, let's just let the primary handle the request.
        if server_instance == 0:
            return True;
        else:
            return False;


