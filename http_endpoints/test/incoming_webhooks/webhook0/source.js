// This function is the webhook's request handler.
exports = function(payload, response) {
    // Data can be extracted from the request as follows:

    // Query params, e.g. '?arg1=hello&arg2=world' => {arg1: "hello", arg2: "world"}

    // You can use 'context' to interact with other Realm features.
    // Accessing a value:
    // var x = context.values.get("value_name");

    // Querying a mongodb service:
    const doc = context.services.get("mongodb-atlas").db("PixysOS").collection("users").findOne();

    // Calling a function:
    
    // The return value of the function is sent as the response back to the client
    // when the "Respond with Result" setting is set.
    return  doc;
};