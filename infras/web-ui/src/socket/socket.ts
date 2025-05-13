import { io } from 'socket.io-client';

const Socket = io('http://localhost:5000', {
  transports: ['websocket', 'pooling'],
});

export default Socket;
