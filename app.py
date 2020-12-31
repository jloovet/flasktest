from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

#simple test...

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySecret0601'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)


@socket_.on('vote', namespace='/api')
def vote_handler(vote_data):
    print("printing voting ", vote_data)
    #send to all using broadcast
    emit('vote_result',
    [
        {"voters" : ["kssk", "dsdsd"]},        
        {"voters" : ["kssk"]},
        {"voters" : ["kssk", "dsdsd"]},        
        {"voters" : ["kssk", "dsdsd", "sass"]},
        {"voters" : []},        
        {"voters" : ["!dsd#e#!sd"]}
    ],
   broadcast=True)


if __name__ == '__main__':
    socket_.run(app, debug=True)
