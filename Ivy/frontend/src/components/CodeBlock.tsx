import React, { useState } from 'react';
import {
  Box,
  IconButton,
  Tooltip,
  useTheme,
  alpha
} from '@mui/material';
import {
  ContentCopy as CopyIcon,
  Check as CheckIcon
} from '@mui/icons-material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodeBlockProps {
  code: string;
  language?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language = 'javascript'
}) => {
  const theme = useTheme();
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Box
      sx={{
        position: 'relative',
        borderRadius: 1,
        overflow: 'hidden',
        '&:hover .copy-button': {
          opacity: 1
        }
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          top: 8,
          right: 8,
          zIndex: 1
        }}
        className="copy-button"
      >
        <Tooltip title={copied ? 'Copied!' : 'Copy code'}>
          <IconButton
            size="small"
            onClick={handleCopy}
            sx={{
              bgcolor: alpha(theme.palette.background.paper, 0.1),
              color: theme.palette.grey[300],
              opacity: 0,
              transition: 'opacity 0.2s',
              '&:hover': {
                bgcolor: alpha(theme.palette.background.paper, 0.2)
              }
            }}
          >
            {copied ? <CheckIcon fontSize="small" /> : <CopyIcon fontSize="small" />}
          </IconButton>
        </Tooltip>
      </Box>

      <SyntaxHighlighter
        language={language}
        style={materialDark}
        customStyle={{
          margin: 0,
          padding: '1rem',
          borderRadius: theme.shape.borderRadius,
          fontSize: '0.875rem',
          backgroundColor: alpha(theme.palette.common.black, 0.9)
        }}
      >
        {code}
      </SyntaxHighlighter>
    </Box>
  );
}; 