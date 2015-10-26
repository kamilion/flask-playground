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

# json import so json.dumps(selection) will work instead of jsonify(selection).
# Note: flask's jsonify is still useful for things outside of rethinkdb sequences.
import json

# rethink configuration
from app.config import rdb
# This Class uses database configuration:
cdb = 'chatdb'

# Pull in our local model
from kochat.kochatmodel import KOChat

########################################################################################################################
## View Class
########################################################################################################################
class KOChatView(FlaskView):
    #decorators = [login_required]

    def index(self):
        return render_template('kochat/koindex.html')

    @route('make', methods=['POST'])
    def make(self):
        that_guy = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        message = KOChat.make(that_guy, request.json['name'], request.json['message'])
        return jsonify({"id": message['id'], "message": message['message'],
                    "meta": {"name": message['meta']['name'],
                    "updated_at": message['meta']['updated_at']}})

    def get(self, uuid):
        this_message = r.db(rdb['chatdb']).table('ko_chats').get(uuid).run(g.rdb_conn)
        if this_message is not None:
            print("KOChat.get_json: Retrieved Chat message from DB: {}".format(this_message))
            return jsonify(this_message)
        else:
            return "Not Found", 404

    def get_history(self, past=600):
        selection = find_message_history(int(past))
        if selection is not None:
            print("KOChat.get_history: Retrieved Chats message from DB: {}".format(selection))
            return jsonify(messages=selection)
        else:
            return "Not Found", 404

    def today(self):
        selection = find_message_history(past=86400)
        if selection is not None:
            print("KOChat.today: Retrieved Chat messages from DB: {}".format(selection))
            return jsonify(messages=selection)
        else:
            return "Not Found", 404

    def this_week(self):
        selection = find_message_history(past=604800)
        if selection is not None:
            print("KOChat.this_week: Retrieved Chat messages from DB: {}".format(selection))
            return jsonify(messages=selection)
        else:
            return "Not Found", 404

    def this_month(self):
        selection = find_message_history(past=2592000)
        if selection is not None:
            print("KOChat.this_month: Retrieved Chat messages from DB: {}".format(selection))
            return jsonify(messages=selection)
        else:
            return "Not Found", 404


########################################################################################################################
## Helper Functions
########################################################################################################################
def find_message_history(past=600):
  selection = list(r.db(rdb['chatdb']).table('ko_chats').filter(
      lambda this_message: this_message.has_fields({'meta': {'name': True}})
  ).filter(
      lambda this_message: this_message.has_fields({'meta': {'updated_at': True}})
  ).filter(
      r.row['meta']['updated_at'].during(r.now() - int(past), r.now() + 3600)
  ).order_by(
      r.desc(r.row['meta']['updated_at'])
  ).run(g.rdb_conn))
  if selection is not None:
      #print("KOChat.find_message_history: Retrieved Chats message from DB: {}".format(selection))
      return selection
  else:
      return []

