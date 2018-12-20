# HyperledgerWebservice
This repository is home to a series of programs I worked on with Joseph Collins to develop a Spyne-based SOAP service that depends on Hyperledger both for Load Balancing and request logging.

We made two contributions to the existing methods of SOAP and Hyperledger.  
The first contribution was through our development of msoap.py, which can be found in the Client-Side folder.  While this is specified to our system, its model can be adapted for any required SOAP multicast.  
The second contribution was through our development of hlsi.py, which can be found in the Server-Side folder.  The HLSI allows our SOAP servers to interact with a Hyperledger framework (as specificed in the model.cto) through Javascript.  The contributions can be found in both the .js scrips in the folder and the python-cross-javascript implementation.