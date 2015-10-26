
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
## KOIrc Class
########################################################################################################################

# This class represents a IRC-like message in RethinkDB.
class KOIrc(Model):
    # Convenience method
    @classmethod
    def make(cls, source, name, message):
        """
        Create a new KOIrc message entry.
        Remodel itself has a create() call, we need to provide data for it to store.
        @return: A KOIrc object instantiated from the supplied data or None.
        """
        meta = {'source': source, 'name': name, 'updated_at': r.now()}
        print('KOIRCMODEL: Make: metadata: {}, message:\n{} '.format(meta, message))
        try:  # To make the database entry with the meta data.
            the_new_message = KOIrc.create(meta=meta, message=message) 
        except KeyError:
            return None
        print('KOIRCMODEL: Make SUCCESS: metadata: {}, message:\n{} '.format(meta, message))
        return the_new_message

    def __repr__(self):
        return '<KOIrc message {} Source: {} Name: {}>'.format(
            self['id'], self['source'], self['name'])


# Call this to populate the tables if they don't exist.
create_tables()
# Call this to populate the indexes if they don't exist.
create_indexes()
