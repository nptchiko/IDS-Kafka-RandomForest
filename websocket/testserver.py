import socketio

sio = socketio.Client()

@sio.on('initial_data')
def on_initial_data(data):
    print('Received initial data:', data)

@sio.on('updated_data')
def on_updated_data(data):
    print('Received updated data:', data)

try:
    sio.connect('http://localhost:5000')  # Connect to your server
    sio.emit('refresh')  # Trigger the refresh event
    sio.wait()  # Wait for incoming events
except KeyboardInterrupt:
    print("Process interrupted. Closing connection.")
    sio.disconnect()  # Gracefully disconnect the client
