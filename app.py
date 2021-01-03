from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

#class to gather result
class VoteRoom :
    def __init__(self, subject):
        #create 6 empty lists
        self.result = [[] for _ in range(6)]
        self.subject = subject

    def to_json_obj(self):
        #create an object that emit could turn into json
        result_field = []
        for voters in self.result:
            result_field.append({"voters": voters})
        return {"result": result_field, "subject": self.subject}    

    def add_vote(self, voter, option):
        self.result[option].append(voter)


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySecret0601'
socket_ = SocketIO(app, async_mode='eventlet')
thread = None
thread_lock = Lock()

room = VoteRoom("test")

@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)

#client sends connct by default at init
@socket_.on('connect', namespace='/api')
def connect():    
    update_clients()

@socket_.on('vote', namespace='/api')
def vote_handler(vote_data):
    print("printing voting ", vote_data)
    room.add_vote(vote_data["name"], vote_data["option"])
    #send to all using broadcast
    update_clients()

@socket_.on('create_new', namespace='/api')
def create_new(subject_data):
    global room
    room = VoteRoom(subject_data["subject"])
    update_clients()

def update_clients() :
    emit('vote_result', room.to_json_obj(), broadcast=True)

if __name__ == '__main__':
    socket_.run(app, debug=True, host="0.0.0.0")
