import os

# Need to read ENV variables for DB connection
HOST = os.environ['DBHOST'] if 'DBHOST' in os.environ else "127.0.0.1"
USER = os.environ['DBUSER'] if 'DBUSER' in os.environ else "doug"
PASSWORD = os.environ['DBPASSWORD'] if 'DBPASSWORD' in os.environ else "letmein!"
DATABASE = os.environ['DBDATABASE'] if 'DBDATABASE' in os.environ else "eventsdb"
