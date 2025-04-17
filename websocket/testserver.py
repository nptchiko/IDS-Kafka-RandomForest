import socketio

sio = socketio.Client()

@sio.on('initial_data')
def on_initial_data(data):
    print('Received initial data:', data)

sio.connect('http://localhost:5000')
print("Connected to server.")
sio.wait()
