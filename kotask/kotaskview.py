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
from kotask.kotaskmodel import KOTask

########################################################################################################################
## View Class
########################################################################################################################
class KOTaskView(FlaskView):
    #decorators = [login_required]

    def index(self):
        return render_template('kotask/koindex.html')

    @route('make', methods=['POST'])
    def make(self):
        message = KOTask.make(request.json['title'], request.json['description'])
        return jsonify({"title": request.json['title'],
                    "description": request.json['description'],
                    "id": message['id']})

    def get(self, uuid):
        this_message = r.db(rdb['chatdb']).table('ko_tasks').get(uuid).run(g.rdb_conn)
        if this_message is not None:
            print("KOTask.get_json: Retrieved Chat message from DB: {}".format(this_message))
            return jsonify(this_message)
        else:
            return "Not Found", 404

    def list(self):
        selection = find_tasks(past=2592000)
        if selection is not None:
            print("KOTask.list: Retrieved Tasks from DB: {}".format(selection))
            return jsonify(tasks=selection)
        else:
            return "Not Found", 404

    def today(self):
        selection = find_tasks(past=86400)
        if selection is not None:
            print("KOTask.today: Retrieved Tasks from DB: {}".format(selection))
            return jsonify(tasks=selection)
        else:
            return "Not Found", 404

    def this_week(self):
        selection = find_tasks(past=604800)
        if selection is not None:
            print("KOTask.this_week: Retrieved Tasks from DB: {}".format(selection))
            return jsonify(tasks=selection)
        else:
            return "Not Found", 404

    def this_month(self):
        selection = find_tasks(past=2592000)
        if selection is not None:
            print("KOTask.this_month: Retrieved Tasks from DB: {}".format(selection))
            return jsonify(tasks=selection)
        else:
            return "Not Found", 404


########################################################################################################################
## Helper Functions
########################################################################################################################
def find_tasks(past=600):
  selection = list(r.db(rdb['chatdb']).table('ko_tasks').filter(
      lambda this_message: this_message.has_fields({'title': True})
  ).filter(
      lambda this_message: this_message.has_fields({'updated_at': True})
  ).filter(
      r.row['updated_at'].during(r.now() - int(past), r.now() + 3600)
  ).order_by(
      r.desc(r.row['updated_at'])
  ).run(g.rdb_conn))
  if selection is not None:
      #print("KOTask.find_tasks: Retrieved Tasks from DB: {}".format(selection))
      return selection
  else:
      return []

