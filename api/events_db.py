from pickle import NONE
from config import DATABASE, USER, PASSWORD, HOST
import psycopg2

MOCK_EVENTS = { "events": [
{'id': 1, 'title': 'Mock Pet Show', 'event_time': 'June 6 at Noon', 'description': 'Super-fun with furry friends!', 'location': 'Reston Dog Park', 'likes': 10},
{'id': 2, 'title': 'Mock Python Course', 'event_time': 'Tomorrow', 'description': 'Coding without the curly braces', 'location': 'Training Room 1', 'likes': 20},
]
}

DB_EVENTS = {"events": []}

def getConnection():
    return psycopg2.connect(database=DATABASE, 
    user = USER, 
    password = PASSWORD, 
    host = HOST, 
    port = "5432")

class Events_DB:

    def getAllEvents(self):
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

    def addEvent(self, data, user_email):
        insert_sql = """
        INSERT INTO events (title, event_time, description, location) 
        VALUES (%s, %s, %s, %s) 
        RETURNING id;
        """
        title = ""
        event_time = ""
        description = ""
        location = ""
        id = NONE

        try:
            title = data["title"]
            event_time = data["event_time"]
            description = data["description"]
            location = data["location"]
        except:
            return "Client Error", 400

        try:
            conn = getConnection()
            cur = conn.cursor()
            cur.execute(insert_sql, (title, event_time, description, location,))
            id = cur.fetchone()[0]
            print(id)
            conn.commit()
            print("Executed SQL Statement: {0}".format(insert_sql))

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
            print("Executed SQL Statement: {0}".format(insert_sql))
            return ev
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Server Error", 500


    def getEventByID(self, event_id, action):
        get_likes_sql = "SELECT likes from events WHERE id = %s;"
        update_likes_sql = "UPDATE events SET likes = %s WHERE id = %s"
        sql = """
        SELECT id, title, event_time, description, location, likes, datetime_added 
        FROM events
        WHERE id = %s;"""
        
        conn = getConnection()
        cur = conn.cursor()
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
            return None

    def deleteEventByID(self, event_id):
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

    def deleteAllEventsExceptOne(self):
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM events WHERE id > 1;"
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            print("Executed SQL Statement: {0}".format(sql))
            return "", 204
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Record not found", 404

    def countEvents(self):
        try:
            conn = getConnection()
            cur = conn.cursor()
            sql = "SELECT COUNT(id) as count FROM EVENTS;"
            cur.execute(sql)
            row = cur.fetchone()
            count = row[0]
            cur.close()
            conn.close()
            print("Executed SQL Statement: {0}".format(sql))
            return count
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "Server Error", 500