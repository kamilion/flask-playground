// Create a top level function to acquire data from the server.
function GetJSONReply(endpoint) {
    $.getJSON(endpoint, function(jreply) {
	console.log("Got reply: " + ko.toJSON(jreply));
	return jreply;
    });
}

// Get the initial data from the server.
var the_reply = GetJSONReply('/koirc/get_history/60');

// This isn't used yet.
var viewModel = ko.mapping.fromJS(the_reply);

// finally, apply the bindings to the page.
ko.applyBindings(viewModel);
console.log("KOTempViewModel applied bindings.");
