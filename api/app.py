from flask import Flask
from flask_restful import Api
from flask import jsonify
from events import EventsList, Event

app = Flask(__name__)
api = Api(app)

api.add_resource(EventsList, '/events')
api.add_resource(Event, '/events/<event_id>')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082, debug=True)