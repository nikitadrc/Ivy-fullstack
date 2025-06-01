import React from 'react';
import {
  Box,
  Paper,
  Typography,
  useTheme,
  alpha
} from '@mui/material';
import { motion } from 'framer-motion';
import { CodeBlock } from './CodeBlock';
import { Person as UserIcon, SmartToy as BotIcon } from '@mui/icons-material';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
  isUser: boolean;
}

const messageVariants = {
  initial: {
    opacity: 0,
    y: 20,
    scale: 0.95,
  },
  animate: {
    opacity: 1,
    y: 0,
    scale: 1,
  },
  exit: {
    opacity: 0,
    y: -20,
    scale: 0.95,
  },
};

const messageTransition = {
  type: 'spring',
  stiffness: 500,
  damping: 30,
};

const extractCodeBlocks = (content: string) => {
  const regex = /```(\w+)?\n([\s\S]*?)```/g;
  const parts: { type: 'text' | 'code'; content: string; language?: string }[] = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(content)) !== null) {
    // Add text before code block
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex, match.index)
      });
    }

    // Add code block
    parts.push({
      type: 'code',
      language: match[1] || 'plaintext',
      content: match[2].trim()
    });

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < content.length) {
    parts.push({
      type: 'text',
      content: content.slice(lastIndex)
    });
  }

  return parts;
};

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  isUser
}) => {
  const theme = useTheme();
  const parts = extractCodeBlocks(message.content);

  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={messageVariants}
      transition={messageTransition}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: isUser ? 'row-reverse' : 'row',
          gap: 1,
          alignItems: 'flex-start',
          mb: 2
        }}
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{
            type: 'spring',
            stiffness: 500,
            damping: 25,
            delay: 0.1
          }}
        >
          <Box
            sx={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: isUser
                ? alpha(theme.palette.primary.main, 0.1)
                : alpha(theme.palette.secondary.main, 0.1),
              color: isUser
                ? theme.palette.primary.main
                : theme.palette.secondary.main,
              boxShadow: theme.shadows[2]
            }}
          >
            {isUser ? <UserIcon /> : <BotIcon />}
          </Box>
        </motion.div>

        <Paper
          elevation={2}
          sx={{
            maxWidth: '80%',
            p: 2,
            bgcolor: isUser
              ? alpha(theme.palette.primary.main, 0.05)
              : alpha(theme.palette.secondary.main, 0.05),
            borderRadius: 2,
            position: 'relative',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 12,
              [isUser ? 'right' : 'left']: -8,
              width: 0,
              height: 0,
              borderStyle: 'solid',
              borderWidth: '8px 8px 8px 0',
              borderColor: `transparent ${isUser 
                ? alpha(theme.palette.primary.main, 0.05)
                : alpha(theme.palette.secondary.main, 0.05)} transparent transparent`,
              transform: isUser ? 'scaleX(-1)' : 'none'
            }
          }}
        >
          {parts.map((part, index) => (
            <Box key={index} sx={{ mb: part.type === 'code' ? 2 : 1 }}>
              {part.type === 'text' ? (
                <Typography
                  variant="body1"
                  sx={{
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    lineHeight: 1.6
                  }}
                >
                  {part.content}
                </Typography>
              ) : (
                <CodeBlock
                  code={part.content}
                  language={part.language}
                />
              )}
            </Box>
          ))}

          <Typography
            variant="caption"
            sx={{
              display: 'block',
              mt: 1,
              color: 'text.secondary',
              textAlign: isUser ? 'right' : 'left',
              opacity: 0.8
            }}
          >
            {new Date(message.timestamp).toLocaleTimeString()}
          </Typography>
        </Paper>
      </Box>
    </motion.div>
  );
}; 