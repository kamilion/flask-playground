
__author__ = 'Kamilion@gmail.com'
########################################################################################################################
## Imports
########################################################################################################################

# Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# Flask-login imports
from flask.ext.login import login_user, logout_user, current_user, login_required

# Flask-classy imports
from flask.ext.classy import FlaskView, route

########################################################################################################################
## View Class
########################################################################################################################
class BaseView(FlaskView):
    route_base = '/'

    def index(self):
        return redirect(url_for('CalcView:csscalc'))

