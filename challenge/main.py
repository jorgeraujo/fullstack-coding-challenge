from challenge import create_app, socketio
import eventlet
from flask_cors import CORS
eventlet.monkey_patch()
app = create_app()
CORS(app)

if __name__ == '__main__':
    socketio.run(app)