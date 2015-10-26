
__author__ = 'Kamilion@gmail.com'
########################################################################################################################
## Site Specific Configuration Definitions
########################################################################################################################


########################################################################################################################
## Flask Configuration Definitions
########################################################################################################################

# CSRF protection
secret_key = "isaidcomeonfhqwhgadseverybodytothelimitthecheatistothelimiteverybodycomeonfhqwhgads"

# API Endpoint protection
api_key = "fhqwhgads"

# Debugging?
debug = True

########################################################################################################################
## Mail Host Configuration Definitions
########################################################################################################################
# smtplib config
smtp = {
    'host': 'mail.m-cubed.com',
    'port': 587,
    'tls': True,
    'replyto': 'mteam@m-cubed.com',  # Must be an email address. Messages will originate here by default.
    'username': 'm3\m3webserver',  # Must be a username (MS Exchange likes <domain>\<username> )
    'password': 'zblWrxCqWJce4Ad2',
}

########################################################################################################################
## RethinkDB Configuration Definitions
########################################################################################################################
# rethink config
rdb = {
    'host': 'localhost',
    'port': 28015,
    'auth_key': '158bcmcubed',
    'defaultdb': 'calc_chat',
    'chatdb': 'calc_chat',
}

# Note, there is currently a bug with how remodel handles databases. Stick to one for now.

