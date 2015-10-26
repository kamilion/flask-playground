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

    $.getJSON('/kochat/this_month/', function(messageModels) {
	var t = $.map(messageModels.messages, function(item) {
	    return new ChatMessage(item);
	});
	self.messages(t);
    });

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
		console.log("Server indicated success, Pushing to messages array");
		self.messages.push(new ChatMessage({ id: data.id, name: data.name, message: data.message}));
		return;
	    },
	    error: function() {
		return console.log("Failed");
	    }
	});
    };
}

var kocvm = new KOChatViewModel()
ko.applyBindings(kocvm);