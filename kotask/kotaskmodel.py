
__author__ = 'Kamilion@gmail.com'
########################################################################################################################
## Imports
########################################################################################################################

# Rethink imports
import rethinkdb as r

# Rethink configuration
#from app.config import rdb

# Import the remodel connection class so we can influence it's configuration, as we need to set the db and auth_key.
import remodel.connection
#remodel.connection.pool.configure(db=rdb['chatdb'],  # This db holds the 'billing' table.
# host=rdb['host'], port=rdb['port'], auth_key=rdb['auth_key'])
remodel.connection.pool.configure(db='calc_chat', auth_key='158bcmcubed')



# Import the actual Model superclass.
from remodel.models import Model
from remodel.utils import create_tables, create_indexes

# Import regex support
import re

########################################################################################################################
## KOTask Class
########################################################################################################################

# This class represents a Task in RethinkDB.
class KOTask(Model):
    # Convenience method
    @classmethod
    def make(cls, title, description):
        """
        Create a new KOTask entry.
        Remodel itself has a create() call, we need to provide data for it to store.
        @return: A KOTask object instantiated from the supplied data or None.
        """
        print('KOTASKMODEL: Make: title: {}, description:\n{} '.format(title, description))
        try:  # To make the database entry with the meta data.
            the_new_task = KOTask.create(title=title, description=description, updated_at=r.now()) 
        except KeyError:
            return None
        print('KOTASKMODEL: Make SUCCESS: title: {}, description:\n{} '.format(title, description))
        return the_new_task

    def __repr__(self):
        return '<KOTask {} Title: {} Description: {}>'.format(
            self['id'], self['title'], self['description'])


# Call this to populate the tables if they don't exist.
create_tables()
# Call this to populate the indexes if they don't exist.
create_indexes()
