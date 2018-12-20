let rid = process.argv[2]                                                                                                                                                                                           
let server = process.argv[3]                                                                                                                                                                                        
let load = parseFloat(process.argv[4])                                                                                                                                                                              
let ip = process.argv[5]                                                                                                                                                                                            
let operation = process.argv[6]                                                                                                                                                                                    
                                                                                                                                                                                                                    

                                                                                                                                                                                                                    
const BusinessNetworkConnection = require('composer-client').BusinessNetworkConnection;                                                                                                                             
var cardname = 'admin@641net';                                                                                                                                                                                      
                                                                                                                                                                                                                    
async function func() {                                                                                                                                                                                             
    let bizNetworkConnection = new BusinessNetworkConnection();                                                                                                                                                     
                                                                                                                                                                                                                    
    let businessNetworkDefinition = await bizNetworkConnection.connect(cardname);                                                                                                                                   
                                                                                                                                                                                                                    
    let requestReg = await bizNetworkConnection.getAssetRegistry('org.example.osnet.Request');                                                                                                                      
    let factory = businessNetworkDefinition.getFactory();                                                                                                                                                           
                                                                                                                                                                                                                    
                                                                                                                                                                                  
    let serverRelationship = factory.newRelationship('org.example.osnet', 'Server', 'org.example.osnet.Server');                                                                                                            
                                                                                                                                                                                                                    
                                                                                                                                                                                                                    
                                                                                                                                                                                                                    
    console.log(rid);                                                                                                                                                                                               
    let request = factory.newResource('org.example.osnet', 'Request', rid);                                                                                                                                         
    request.requestID=rid;                                                                                                                                                                                          
    request.servingInstance=server;                                                                                                                                                                                 
    request.serverLoad = load;                                                                                                                                                                                      
    request.operation = operation;                                                                                                                                                                                  
    request.ip = ip;                                                                                                                                                                                                
    request.timeToLive = 5;                                                                                                                                                                                         
    request.owner = serverRelationship;                                                                                                                                                                             
                                                                                                                                                                                                                    
    await requestReg.add(request);                                                                                                                                                                                  
                                                                                                                                                                                                                    
    process.stdout.write("1");                                                                                                                                                                                      
    process.exit();                                                                                                                                                                                                 
}                                                                                                                                                                                                                   
                                                                                                                                                                                                                    
func();
"node createAsset.js arg arg arg"
