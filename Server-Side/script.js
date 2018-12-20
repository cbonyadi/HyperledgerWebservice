/**
 * Track the trade of a commodity from one trader to another
 * @param {org.example.mynetwork.Trade} trade - the trade to be processed
 * @transaction
 */
async function requestService(request) {
    // loop over participants and set owner based on load
    request.myRequest.serverHandlingRequest = request.newServer;
    let assetRegistry = await getAssetRegistry('org.example.osnet.Server');
    await assetRegistry.update(trade.commodity);
}
