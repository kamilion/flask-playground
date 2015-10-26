// Create an object that will represent a instance of a single message.
function ChatMessage(data) {
    this.id = ko.observable(data.id);
    this.message = ko.observable(data.message);
    this.meta = ko.observable(data.meta);
}
/*
function ShowClock() {
    var self = this;

    this.clock = ko.observable(new Date());

    this.tick = function() {
        self.clock(new Date());
    };

    setInterval(self.tick, 3000);
};

ko.applyBindings(new ShowClock());

function ShowTimer() {
    var self = this;
        
    self.timer = ko.observable(60);
     
    setInterval(function() {
        var newTimer = self.timer() - 1;
        self.timer(newTimer <= 0 ? 60 : newTimer);
    }, 1000);
};

ko.applyBindings(new ShowTimer());

*/

// Create a model that will represent multiple instances of ChatMessage.
function KOChatViewModel() {
    var self = this;
    // Create a message buffer.
    self.messages = ko.observableArray([]);
    // Create the observables users will interact with on the page.
    self.newMessage = ko.observable();
    self.newName = ko.observable();

    self.clock = ko.observable(new Date());
    self.tick = function() {
        self.clock(new Date());
    };
    setInterval(self.tick, 1000);

    self.timer = ko.observable(10);
    self.tock = function() {
        var newTimer = self.timer() - 1;
        self.timer(newTimer <= 0 ? 10 : newTimer);
    }
    setInterval(self.tock, 1000);

    self.alarm = function() {
        GetJSONReply('/koirc/get_history/60');
    }
    setInterval(self.alarm, 10000);


    // Create a function to be called when submit is clicked.
    self.addMessage = function() {
	self.save();
	self.newMessage("");
	// self.newName("");
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
	    url: '/koirc/make',
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
var the_reply = GetJSONReply('/koirc/get_history/60');

// This isn't used yet.
var viewModel = ko.mapping.fromJS(the_reply);

// finally, apply the bindings to the page.
ko.applyBindings(kocvm);
console.log("KOChatViewModel applied bindings.");
