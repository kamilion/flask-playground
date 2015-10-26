// Create an object that will represent a instance of a single message.
function ChatMessage(data) {
    this.id = ko.observable(data.id);
    this.message = ko.observable(data.message);
    this.meta = ko.observable(data.meta);
}

// Create a model that will represent multiple instances of ChatMessage.
function KOChatViewModel() {
    var self = this;
    // Create a message buffer.
    self.messages = ko.observableArray([]);
    // Create the observables users will interact with on the page.
    self.newMessage = ko.observable();
    self.newName = ko.observable();

    // Create a function to be called when submit is clicked.
    self.addMessage = function() {
	self.save();
	self.newMessage("");
	self.newName("");
    };

    // Create a function to be called when we receive multiple messages.
    self.eatMessage = function(jreply) {
	var t = $.map(jreply.messages, function(item) {
	    return new ChatMessage(item);
	});
	self.messages(t);
    }

    // Create a function to be called when we need to submit a new message to the server.
    self.save = function() {
	return $.ajax({
	    url: '/kochat/make',
	    contentType: 'application/json',
	    type: 'POST',
	    data: JSON.stringify({
		'name': self.newName(),
		'message': self.newMessage()
	    }),
	    success: function(data) {
		// Stuff the new message directly into the message buffer.
		self.messages.unshift(new ChatMessage({ id: data.id, message: data.message , meta: data.meta }));
		return console.log("KOCVM: Server indicated success, Pushing to messages array");
	    },
	    error: function() {
		return console.log("KOCVM: Server indicated failure");
	    }
	});
    };
    console.log("KOChatViewModel Initialized.");
}

// Assign a new instance of the model to a variable.
var kocvm = new KOChatViewModel()

// Create a top level function to acquire data from the server.
function GetJSONReply(endpoint) {
    $.getJSON(endpoint, function(jreply) {
	console.log("Got reply: " + ko.toJSON(jreply));
	kocvm.eatMessage(jreply);
	return jreply;
    });
}

// Get the initial data from the server.
var the_reply = GetJSONReply('/kochat/get_history/3600');

// This isn't used yet.
var viewModel = ko.mapping.fromJS(the_reply);

// finally, apply the bindings to the page.
ko.applyBindings(kocvm);
console.log("KOChatViewModel applied bindings.");
