import time
import psutil
from Naked.toolshed.shell import muterun_js as muterun


#THIS IS A CLASS
class HyperLedgerSoapInteractive:
    hyperledger = None;
    _ip = "";
    
    #init???
    def __init__(self, ip):
        hyperledger = None;
        self._ip = ip;
        #verify that I exist as a participant on the hyperledger infrastructure.
    
    
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
        #timer
        start = time.time()
        #counter
        counter = 0;
	claim_counter = 100;

	if server_instance == 0:
	    self._create_asset(rid,self._ip,psutil.cpu_percent(),ip,function);
        else:
	    time.sleep(6);

        timeout = 12; #12 seconds to deliver to client.
        #while timeout not reached
        while time.time() - start <= timeout:
            #read the hyperledger ~ call JS, read
            asset = self._get_asset(rid);
            #if it does not exist and counter = server_instance, 
            if not asset:
                #create ticket with me as load ~ call JS, create
                self._create_asset(rid,self._ip,psutil.cpu_percent(),ip,function);
            #if it does exist
            elif asset["isOwned"]:
                break;
            else:
                #if its server isn't me
                if asset["servingInstance"] != self._ip:
                    #if its load < my load
                    if asset["serverLoad"] < psutil.cpu_percent():
			#quit and return false
                        return False;
                    #else
                    else:
                        #set its server to me ~ call JS, change owner
                        #set its load to my load ~ call JS, update my load
			claim_counter = counter;
                        self._claim_asset(rid, self._ip, psutil.cpu_percent());
                elif counter > claim_counter + 2:
		    break;
            #wait a bit
            #This should prevent race conditions, for the most part.
            time.sleep(timeout/(2+server_instance)); 
            
            #increment counter
            counter += 1;
        
        #read the hyperledger for this asset ~ call JS, read
        asset = self._get_asset(rid);
        if asset["servingInstance"] != self._ip:
            #if i'm not assigned, return False
            return False;
        else:
            self._finalize(rid);
	    return True;
            

    def _get_asset(self, rid):
        '''This function will get the an asset by rid from the Hyperledger 
        fabric
    
        Parameters
        ----------
        rid : int
            A decently random he request at the behest of the client.
        
        Returns
        -------
        dict
            If the asset exists in the framework, then this will return a 
            dictionary of the server, its load, and if it's owned.  Otherwise, 
            it will return None. needs load, server
        '''
        args = '%d' % (rid);
        

        output = muterun("./getAsset.js", arguments=args);

	
        out_list = output.stdout.split(",")
        
       	out_dict = {};
        out_dict["servingInstance"] = out_list[0];
        out_dict["serverLoad"] = float(out_list[1]);
        out_dict["isOwned"] = bool(out_list[2]);
        
       	return out_dict;
	
        

    def _create_asset(self, rid, server, load, ip, operation):
        '''This function will get the an asset by rid from the Hyperledger 
        fabric
    
        Parameters
        ----------
        rid : int
            A decently random he request at the behest of the client.
        server : str
            Your IP address.
        load : double
            Your Load.
        ip : str
            The client IP.
        operation : str
            The function called by the client.
        
        Returns
        -------
        Bool
            True if successful, False if not.
        '''
        args = '%d "%s" %d "%s" "%s"' % (rid,server,load,ip,operation);
        
        output = muterun("./createAsset.js", arguments=args);
        
        return bool(output.stdout);
        
            

    def _claim_asset(self, rid, server, load):
        '''This function will get the an asset by rid from the Hyperledger 
        fabric
    
        Parameters
        ----------
        rid : int
            A decently random he request at the behest of the client.
        server : str
            Your IP address.
        load : double
            Your Load.
        
        Returns
        -------
        Bool
            True if successful, False if not.
        '''
        args = '%d "%s" %d' % (rid,server,load);
        
        output = muterun("./createAsset.js", arguments=args);
        
        return bool(output.stdout);
            

    def _finalize(self, rid):
        '''This function will finally set the owner of an Asset to whoever owns it.
    
        Parameters
        ----------
        rid : int
            A decently random he request at the behest of the client.
        
        Returns
        -------
        Bool
            True if it works, False if it doesn't.
        '''
        args = '%d' % (rid);
        
        output = muterun("./finalize.js", arguments=args);
        
        return bool(output.stdout);
        

