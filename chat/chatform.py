
########################################################################################################################
## Imports
########################################################################################################################

# Flask imports
from flask import flash
from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms.fields import TextField, TextAreaField, PasswordField, HiddenField
from wtforms.validators import DataRequired

# Our own Chat model
from chat.chatmodel import Chat

########################################################################################################################
## Class Definitions
########################################################################################################################

class ChatForm(Form):
    """
    A simple Chat form.
    Will create Chat messages and may provide a Chat object, if found, to the View.
    """
    source = HiddenField('source')
    name = TextField('name', validators=[DataRequired()])
    message = TextAreaField('message', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """
        Register a new a Chat object via a Chat class helper
        @param args: Arguments, in order of definition in class
        @param kwargs: Keyword based Arguments, in any order
        """
        Form.__init__(self, *args, **kwargs)
        self.channel = None

    def validate(self):
        """
        Do validation of the form contents.
        @return: True if the Chat object was successfully created, or False if it was not.
        """
        rv = Form.validate(self)
        if not rv:
            flash('A required field is empty', 'error')
            return False

        message = Chat.make(self.source.data, self.name.data, self.message.data)

        if message is not None:
            return True
        else:
            return False

