import { io, Socket } from 'socket.io-client';
import { WSMessage, WSTypingIndicator } from '../types/chat';

class WebSocketService {
  private socket: Socket | null = null;
  private userId: number | null = null;

  connect(userId: number) {
    this.userId = userId;
    this.socket = io(process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000', {
      path: '/ws/chat',
      query: {
        userId: userId.toString()
      }
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  sendTypingIndicator(isTyping: boolean) {
    if (this.socket && this.userId) {
      const message: WSTypingIndicator = {
        type: 'typing',
        user_id: this.userId,
        content: {
          is_typing: isTyping
        }
      };
      this.socket.emit('message', message);
    }
  }

  onTypingIndicator(callback: (data: WSTypingIndicator) => void) {
    if (this.socket) {
      this.socket.on('typing', (data: WSTypingIndicator) => {
        callback(data);
      });
    }
  }

  onMessage(callback: (data: WSMessage) => void) {
    if (this.socket) {
      this.socket.on('message', (data: WSMessage) => {
        callback(data);
      });
    }
  }
}

export const wsService = new WebSocketService(); 