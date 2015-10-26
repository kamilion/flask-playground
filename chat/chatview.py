__author__ = 'Kamilion@gmail.com'
########################################################################################################################
## Imports
########################################################################################################################

# Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

# Flask-login imports
from flask.ext.login import current_user, login_required

# Flask-classy imports
from flask.ext.classy import FlaskView, route

# Flask-WTF imports
from chat.chatform import ChatForm

# rethink imports
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

# rethink configuration
from app.config import rdb
# This Class uses database configuration:
cdb = 'chatdb'

# Pull in our local model
from chat.chatmodel import Chat

########################################################################################################################
## View Class
########################################################################################################################
class ChatView(FlaskView):
    #decorators = [login_required]

    def index(self):
        form = ChatForm()
        form.source.data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return render_template('chat/chatform.html', form=form)

    @route('post_message', methods=['POST'])
    def post_message(self):
        """
        Processing of a User Submitted Chat Flask-WTF form
        @return: A Jinja2 Template containing a Chat form, or a redirect to the index or next page.
        """
        form = ChatForm()
        if form.validate_on_submit():
            flash('Message Sent.', 'success')
            print("Chat.post_message: Posted Chat message to DB: {}".format(form.data))
            return redirect(request.args.get('next') or url_for('ChatView:index'))
        return render_template('chat/chatform.html', form=form)

    def get(self, uuid):
        selection = r.db(rdb['chatdb']).table('chats').get(uuid).run(g.rdb_conn)
        if selection is not None:
            print("Chat.get: Retrieved Chat message from DB: {}".format(selection))
            return render_template('chat/chatmessage.html', results=selection)
        else:
            return "Not Found", 404

    def get_all(self):
        selection = list(r.db(rdb['chatdb']).table('chats').order_by(r.desc(lambda date: date['meta']['updated_at'])).run(g.rdb_conn))
        if selection is not None:
            print("Chat.get_all: Retrieved Chat messages from DB: {}".format(selection))
            return render_template('chat/chatlist.html', results=selection)
        else:
            return "Not Found", 404

    def get_json(self, uuid):
        this_message = r.db(rdb['chatdb']).table('chats').get(uuid).run(g.rdb_conn)
        if this_message is not None:
            print("Chat.get_json: Retrieved Chat message from DB: {}".format(this_message))
            return jsonify(this_message)
        else:
            return "Not Found", 404

    def get_json_history(self, past=600):
        selection = find_message_history(int(past))
        if selection is not None:
            print("Chat.get_json_history: Retrieved Chats message from DB: {}".format(selection))
            return jsonify(messages=selection)
        else:
            return "Not Found", 404

    def get_history(self, past=600):
        selection = find_message_history(int(past))
        if selection is not None:
            print("Chat.get_history: Retrieved Chats message from DB: {}".format(selection))
            return render_template('chat/chatlist.html', results=selection)
        else:
            return "Not Found", 404

    def today(self):
        selection = find_message_history(86400)
        if selection is not None:
            print("Chat.today: Retrieved Chat messages from DB: {}".format(selection))
            return render_template('chat/chatlist.html', results=selection)
        else:
            return "Not Found", 404

    def this_week(self):
        selection = find_message_history(past=604800)
        if selection is not None:
            print("Chat.this_week: Retrieved Chat messages from DB: {}".format(selection))
            return render_template('chat/chatlist.html', results=selection)
        else:
            return "Not Found", 404

    def this_month(self):
        selection = find_message_history(past=2592000)
        if selection is not None:
            print("Chat.this_month: Retrieved Chat messages from DB: {}".format(selection))
            return render_template('chat/chatlist.html', results=selection)
        else:
            return "Not Found", 404


########################################################################################################################
## Helper Functions
########################################################################################################################
def find_message_history(past=600):
  selection = list(r.db(rdb['chatdb']).table('chats').filter(
      lambda this_message: this_message.has_fields({'meta': {'name': True}})
  ).filter(
      lambda this_message: this_message.has_fields({'meta': {'updated_at': True}})
  ).filter(
      r.row['meta']['updated_at'].during(r.now() - int(past), r.now() + 3600)
  ).order_by(
      r.desc(r.row['meta']['updated_at'])
  ).coerce_to('array').run(g.rdb_conn))
  if selection is not None:
      print("Chat.find_message_history: Retrieved Chats message from DB: {}".format(selection))
      return selection
  else:
      return []

