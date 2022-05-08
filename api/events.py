from pickle import NONE
import psycopg2
from flask import request
from flask_restful import Resource
from config import DATABASE, USER, PASSWORD, HOST

MOCK_EVENTS = { "events": [
  {'id': 1, 'title': 'Mock Pet Show', 'event_time': 'June 6 at Noon', 'description': 'Super-fun with furry friends!', 'location': 'Reston Dog Park', 'likes': 10},
  {'id': 2, 'title': 'Mock Python Course', 'event_time': 'Tomorrow', 'description': 'Coding without the curly braces', 'location': 'Training Room 1', 'likes': 20},
]
}

def getConnection():
    return psycopg2.connect(database=DATABASE, 
    user = USER, 
    password = PASSWORD, 
    host = HOST, 
    port = "5432")

DB_EVENTS = {"events": []}

class EventsList(Resource):
    def get(self):
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql = """
            SELECT id, title, event_time, description, location, likes, datetime_added 
            FROM events 
            ORDER BY likes DESC;"""

            cur.execute(sql)
            rows = cur.fetchall()
            DB_EVENTS["events"] = []  
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
                DB_EVENTS["events"].append(ev)
            cur.close()
            conn.close()
            print("Executed SQL Statement: {0}".format(sql))
            return DB_EVENTS
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            # This returns the Mock Data
            return MOCK_EVENTS

    def post(self):
        sql = """
        INSERT INTO events (title, event_time, description, location) 
        VALUES (%s, %s, %s, %s) 
        RETURNING id;
        """
        data = request.get_json(True)
        title = data["title"]
        event_time = data["event_time"]
        description = data["description"]
        location = data["location"]
        id = NONE

        try:
            conn = getConnection()
            cur = conn.cursor()
            cur.execute(sql, (title, event_time, description, location,))
            id = cur.fetchone()[0]
            print("HERE")
            print(id)
            conn.commit()
            print("Executed SQL Statement: {0}".format(sql))

            cur.execute('SELECT id, title, event_time, description, location, likes, datetime_added FROM events WHERE id = %s', (str(id),))
            row = cur.fetchone()
            ev = {
                'id': row[0],
                'title': row[1],
                'event_time': row[2],
                'description': row[3],
                'location': row[4], 
                'likes': row[5],
                'datetime_added': str(row[6])
                }
            cur.close()
            conn.close()
            print("Executed SQL Statement: {0}".format(sql))
            return ev
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Server Error", 500


class Event(Resource):
    def get(self, event_id):
        get_likes_sql = "SELECT likes from events WHERE id = %s;"
        update_likes_sql = "UPDATE events SET likes = %s WHERE id = %s"
        sql = """
        SELECT id, title, event_time, description, location, likes, datetime_added 
        FROM events
        WHERE id = %s;"""
        
        conn = getConnection()
        cur = conn.cursor()

        action = request.args.get("action")
        print("ACTION = {0}".format(action))
        try:
            # Here add a like if the action parameter was passed. 
            if (action is not None) and (str.lower(action) == 'like'):
                cur.execute(get_likes_sql, (event_id,))
                current_likes = cur.fetchone()[0];
                print("Executed SQL Statement: {0}".format(get_likes_sql))
                cur.execute(update_likes_sql, (current_likes + 1, event_id,))
                conn.commit()
                print("Executed SQL Statement: {0}".format(update_likes_sql))

            print(event_id)     
            cur.execute(sql, (event_id,))
            row = cur.fetchone()
            ev = {
                'id': row[0],
                'title': row[1],
                'event_time': row[2],
                'description': row[3],
                'location': row[4], 
                'likes': row[5],
                'datetime_added': str(row[6])
            }
            cur.close()
            conn.close()
            print("Executed SQL Statement: {0}".format(sql))
            return ev
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Record not found", 404

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
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM events WHERE id = %s;"
            cur.execute(sql, (event_id,))
            conn.commit()
            cur.close()
            conn.close()
            print("Executed SQL Statement: {0}".format(sql))
            return "", 204
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Record not found", 404