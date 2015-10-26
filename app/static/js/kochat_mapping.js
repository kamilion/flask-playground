function ChatMessage(data) {
    this.id = ko.observable(data.id);
    this.message = ko.observable(data.message);
    this.meta = ko.observable(data.meta);
}

function KOChatViewModel() {
    var self = this;
    self.messages = ko.observableArray([]);
    self.newMessage = ko.observable();
    self.newName = ko.observable();

    self.addMessage = function() {
	self.save();
	self.newMessage("");
	self.newName("");
    };

    self.eatMessage = function(jreply) {
	var t = $.map(jreply.messages, function(item) {
	    return new ChatMessage(item);
	});
	self.messages(t);
    }

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

var kocvm = new KOChatViewModel()

function GetJSONReply(endpoint) {
    $.getJSON(endpoint, function(jreply) {
	console.log("Got reply: " + ko.toJSON(jreply));
	kocvm.eatMessage(jreply);
	return jreply;
    });
}

var the_reply = GetJSONReply('/kochat/get_history/3600');

var viewModel = ko.mapping.fromJS(the_reply);

ko.applyBindings(kocvm);