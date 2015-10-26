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

########################################################################################################################
## View Class
########################################################################################################################
class KOTempView(FlaskView):
    #decorators = [login_required]

    def index(self):
        return render_template('kotemp/koindex.html', messages={'shit': [1, 2, 3], 'poop':{'shit2': [1, 2]}})

