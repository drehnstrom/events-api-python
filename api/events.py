
from flask import request
from flask_restful import Resource
from config import DATABASE, USER, PASSWORD, HOST
from events_db import Events_DB

class EventsList(Resource):
    # Give me all the Events
    def get(self):
        return Events_DB().getAllEvents()

    def post(self):
        data = request.get_json(True)
        try:
            return Events_DB().addEvent(data)
        except (Exception) as error:
            print(error)
            return "Server Error", 500

class Event(Resource):
    def get(self, event_id):
        action = request.args.get("action")
        print("ACTION = {0}".format(action))
        
        ev = Events_DB().getEventByID(event_id, action)

        if ev is not None:
            return ev
        else:
            return "Record not found", 404  

    def patch(self, event_id):
        pass


    def delete(self, event_id):
        return Events_DB().deleteEventByID(event_id)