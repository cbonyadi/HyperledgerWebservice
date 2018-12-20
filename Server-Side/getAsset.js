let rid = process.argv[2];

const BusinessNetworkConnection = require('composer-client').BusinessNetworkConnection;
var cardname = 'admin@641net';

async function func() {
    let bizNetworkConnection = new BusinessNetworkConnection();                                                                                                                                                     
    let businessNetworkDefinition = await bizNetworkConnection.connect(cardname);                                                                                                                                   
    let requestReg = await bizNetworkConnection.getAssetRegistry('org.example.osnet.Request');                                                                                                                      
    let request = await requestReg.get(rid);                                                                                                                                                                        
    process.stdout.write(request.servingInstance);                                                                                                                                                                  
    process.stdout.write(",");                                                                                                                                                                                      
    process.stdout.write(request.serverLoad.toString());                                                                                                                                                            
    process.stdout.write(",");                                                                                                                                                                                      
    process.stdout.write((!(request.owner.serverID=="org.example.osnet.Server")).toString());                                                                                                                       
    process.exit();                                                                                                                                                                                                 
};                                                                                                                                                                                                                   

func();
