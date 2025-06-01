import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  CircularProgress,
  useTheme,
  Stack,
  Alert,
  Snackbar,
  Button
} from '@mui/material';
import {
  Send as SendIcon,
  Refresh as RetryIcon
} from '@mui/icons-material';
import { QuestionTypeSelector } from './QuestionTypeSelector';
import { VirtualizedChatMessages } from './VirtualizedChatMessages';
import { TypingIndicator } from './TypingIndicator';
import { FeedbackDialog } from './FeedbackDialog';
import { QuestionType, Message, WSTypingIndicator } from '../types/chat';
import { useChatHistory } from '../hooks/useChatHistory';
import { useDebounce } from '../hooks/useDebounce';
import { wsService } from '../services/websocket';

interface ChatInterfaceProps {
  userId: number;
  selectedRole: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  userId,
  selectedRole
}) => {
  const theme = useTheme();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [otherUserTyping, setOtherUserTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [questionType, setQuestionType] = useState<QuestionType>('technical');
  const [showFeedback, setShowFeedback] = useState(false);
  const [lastMessageId, setLastMessageId] = useState<number | null>(null);
  const debouncedInput = useDebounce(input, 500);
  const { data: chatHistory, isLoading: isLoadingHistory } = useChatHistory(userId);

  useEffect(() => {
    if (chatHistory) {
      setMessages(chatHistory.messages.map(msg => ({
        ...msg,
        timestamp: new Date(msg.timestamp)
      })));
    }
  }, [chatHistory]);

  useEffect(() => {
    // Connect to WebSocket
    wsService.connect(userId);

    // Listen for typing indicators from other users
    wsService.onTypingIndicator((data: WSTypingIndicator) => {
      if (data.user_id !== userId) {
        setOtherUserTyping(data.content.is_typing);
      }
    });

    return () => {
      wsService.disconnect();
    };
  }, [userId]);

  // Send typing indicator when user is typing
  useEffect(() => {
    if (debouncedInput) {
      setIsTyping(true);
      wsService.sendTypingIndicator(true);
      const timeout = setTimeout(() => {
        setIsTyping(false);
        wsService.sendTypingIndicator(false);
      }, 1000);
      return () => clearTimeout(timeout);
    }
  }, [debouncedInput, userId]);

  const handleSend = async (retryMessage?: Message) => {
    const messageToSend = retryMessage || {
      role: 'user' as const,
      content: input,
      timestamp: new Date(),
      status: 'sending'
    };

    if (!retryMessage) {
      setMessages(prev => [...prev, messageToSend]);
      setInput('');
    } else {
      setMessages(prev => 
        prev.map(msg => 
          msg === retryMessage ? { ...msg, status: 'sending' } : msg
        )
      );
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/chat/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question_type: questionType,
          chat_history: messages.map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: data.id,
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        status: 'sent'
      };

      setMessages(prev => 
        prev.map(msg => 
          msg === messageToSend ? { ...msg, status: 'sent' } : msg
        ).concat(assistantMessage)
      );
      
      setLastMessageId(data.id);
      setShowFeedback(true);
    } catch (error) {
      setError('Failed to send message. Please try again.');
      setMessages(prev => 
        prev.map(msg => 
          msg === messageToSend ? { ...msg, status: 'error' } : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = (message: Message) => {
    handleSend(message);
  };

  const handleFeedbackSubmit = async (feedback: {
    rating: number;
    wasHelpful: boolean;
    comment: string;
  }) => {
    if (lastMessageId) {
      try {
        const response = await fetch(`/api/chat/${lastMessageId}/feedback`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(feedback)
        });

        if (!response.ok) {
          throw new Error('Failed to submit feedback');
        }
      } catch (error) {
        setError('Failed to submit feedback. Please try again.');
      }
    }
    setShowFeedback(false);
  };

  if (isLoadingHistory) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ 
      height: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      maxHeight: {
        xs: 'calc(100vh - 56px)',
        sm: 'calc(100vh - 64px)'
      }
    }}>
      <QuestionTypeSelector
        value={questionType}
        onChange={setQuestionType}
      />
      
      <Paper
        elevation={3}
        sx={{
          flex: 1,
          mb: 2,
          p: { xs: 1, sm: 2 },
          overflowY: 'hidden',
          bgcolor: 'background.default'
        }}
      >
        <VirtualizedChatMessages
          messages={messages}
          isLoading={isLoading}
        />
        {messages.map((message, index) => (
          message.status === 'error' && (
            <Box key={`retry-${index}`} sx={{ display: 'flex', justifyContent: 'center', mt: 1 }}>
              <Button
                startIcon={<RetryIcon />}
                onClick={() => handleRetry(message)}
                color="error"
                variant="outlined"
                size="small"
              >
                Retry Message
              </Button>
            </Box>
          )
        ))}
        {(isTyping || otherUserTyping) && (
          <Box sx={{ mt: 2, ml: 2 }}>
            <TypingIndicator />
          </Box>
        )}
      </Paper>

      <Box sx={{ 
        display: 'flex', 
        gap: 1,
        position: 'sticky',
        bottom: 0,
        bgcolor: 'background.default',
        p: { xs: 1, sm: 0 },
        borderTop: { xs: 1, sm: 0 },
        borderColor: 'divider'
      }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Type your question..."
          variant="outlined"
          disabled={isLoading}
          sx={{ 
            bgcolor: 'background.paper',
            '& .MuiOutlinedInput-root': {
              fontSize: { xs: '0.875rem', sm: '1rem' }
            }
          }}
        />
        <IconButton
          onClick={() => handleSend()}
          disabled={isLoading || !input.trim()}
          color="primary"
          sx={{
            bgcolor: theme.palette.primary.main,
            color: 'white',
            width: 48,
            height: 48,
            '&:hover': {
              bgcolor: theme.palette.primary.dark
            }
          }}
        >
          <SendIcon />
        </IconButton>
      </Box>

      <FeedbackDialog
        open={showFeedback}
        onClose={() => setShowFeedback(false)}
        onSubmit={handleFeedbackSubmit}
      />

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
        anchorOrigin={{ 
          vertical: 'bottom', 
          horizontal: 'center'
        }}
        sx={{
          mb: { xs: '72px', sm: '24px' }
        }}
      >
        <Alert 
          onClose={() => setError(null)} 
          severity="error"
          sx={{ 
            width: '100%',
            maxWidth: { xs: '100%', sm: 400 }
          }}
        >
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
}; 