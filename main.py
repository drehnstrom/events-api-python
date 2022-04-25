from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import os
import psycopg2
import json

app = Flask(__name__)
api = Api(app)

# Need to read ENV variables for DB connection
HOST = os.environ['DBHOST'] if 'DBHOST' in os.environ else "127.0.0.1"
USER = os.environ['DBUSER'] if 'DBUSER' in os.environ else "doug"
PASSWORD = os.environ['DBPASSWORD'] if 'DBPASSWORD' in os.environ else "letmein!"
DATABASE = os.environ['DBDATABASE'] if 'DBDATABASE' in os.environ else "eventsdb"

print(HOST)
print(USER)
print(PASSWORD)
print(DATABASE)


MOCK_EVENTS = { "events": [
  {'id': 1, 'title': 'Mock Pet Show', 'event_time': 'June 6 at Noon', 'description': 'Super-fun with furry friends!', 'location': 'Reston Dog Park', 'likes': 10},
  {'id': 2, 'title': 'Mock Python Course', 'event_time': 'Tomorrow', 'description': 'Coding without the curly braces', 'location': 'Training Room 1', 'likes': 20},
]
}

DB_EVENTS = {"events": []}

class EventsList(Resource):
    def get(self):
        try:
            conn = psycopg2.connect(database=DATABASE, user = USER, password = PASSWORD, host = HOST, port = "5432")
            print("Opened database successfully")
            cur = conn.cursor()
            sql = 'SELECT id, title, event_time, description, location, likes, datetime_added FROM events;'
            print(sql)
            cur.execute(sql)
            rows = cur.fetchall()
            DB_EVENTS['events'] = []  
            for row in rows:
                ev = {
                    'id': row[0],
                    'title': row[1],
                    'event_time': row[2],
                    'description': row[3],
                    'location': row[4], 
                    'likes': row[5],
                    'datetime_added': str(row[6])
                }
                DB_EVENTS['events'].append(ev)
            conn.close()
            return DB_EVENTS
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            # This returns the Mock Data
            return MOCK_EVENTS

    def post(self):
        pass
        """ data = request.get_json(True)
        event_id = int(max(MOCK_EVENTS.keys())) + 1
        event_id = '%i' % event_id
        MOCK_EVENTS[event_id] = {
            "title": data["title"],
            "event_time": data["event_time"],
            "description": data["description"],
            "location": data["location"],
            "likes": 0,

        }
        return MOCK_EVENTS[event_id], 201 """


class Event(Resource):
    def get(self, event_id):
        try:
            conn = psycopg2.connect(database=DATABASE, user = USER, password = PASSWORD, host = HOST, port = "5432")
            print("Opened database successfully")
            cur = conn.cursor()
            sql = 'SELECT id, title, event_time, description, location, likes, datetime_added FROM events WHERE id = %s;'
            print(sql)
            cur.execute(sql, (event_id))
            row = cur.fetchone()
            DB_EVENTS['events'] = []  
            ev = {
                'id': row[0],
                'title': row[1],
                'event_time': row[2],
                'description': row[3],
                'location': row[4], 
                'likes': row[5],
                'datetime_added': str(row[6])
            }
            DB_EVENTS['events'].append(ev)
            conn.close()
            return DB_EVENTS
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            # This returns the Mock Data
            return MOCK_EVENTS


    def patch(self, event_id):
        pass
        """ data = request.get_json(True)
        if event_id not in MOCK_EVENTS:
            return "Record not found", 404
        else:
            event = MOCK_EVENTS[event_id]
            if "title" in data:
                event["title"] = data["title"]
            if "event_time" in data:
                event["event_time"] = data["event_time"]
            if "description" in data:
                event["description"] = data["description"]
            if "location" in data:
                event["location"] = data["location"]
            return event, 200 """

    def delete(self, event_id):
        pass
        """  if event_id not in MOCK_EVENTS:
            return "Record not found", 404
        else:
            del MOCK_EVENTS[event_id]
            return '', 204 """


api.add_resource(EventsList, '/events')
api.add_resource(Event, '/events/<event_id>')


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)