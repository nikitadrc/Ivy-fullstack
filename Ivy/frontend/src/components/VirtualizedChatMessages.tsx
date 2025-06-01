import React from 'react';
import { FixedSizeList as List } from 'react-window';
import AutoSizer from 'react-virtualized-auto-sizer';
import { Box } from '@mui/material';
import { ChatMessage } from './ChatMessage';
import { Message } from '../types/chat';

interface VirtualizedChatMessagesProps {
  messages: Message[];
  isLoading: boolean;
}

const ITEM_SIZE = 100; // Base height for messages, will auto-adjust

const MessageRow = React.memo(({ data, index, style }: any) => {
  const message = data.messages[index];
  return (
    <Box style={style} sx={{ py: 1 }}>
      <ChatMessage
        message={message}
        isUser={message.role === 'user'}
      />
    </Box>
  );
});

export const VirtualizedChatMessages: React.FC<VirtualizedChatMessagesProps> = ({
  messages,
  isLoading
}) => {
  const listRef = React.useRef<any>(null);

  React.useEffect(() => {
    // Scroll to bottom when new messages arrive
    if (listRef.current && messages.length > 0) {
      listRef.current.scrollToItem(messages.length - 1, 'end');
    }
  }, [messages.length]);

  return (
    <Box sx={{ flex: 1, height: '100%' }}>
      <AutoSizer>
        {({ height, width }) => (
          <List
            ref={listRef}
            height={height}
            width={width}
            itemCount={messages.length}
            itemSize={ITEM_SIZE}
            itemData={{ messages }}
            overscanCount={5} // Number of items to render beyond visible area
          >
            {MessageRow}
          </List>
        )}
      </AutoSizer>
    </Box>
  );
}; 