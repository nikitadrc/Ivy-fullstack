import React from 'react';
import { Box, useTheme, alpha } from '@mui/material';
import { motion } from 'framer-motion';

interface TypingIndicatorProps {
  isVisible: boolean;
}

const dotVariants = {
  initial: {
    y: 0,
  },
  animate: {
    y: [-2, 2, -2],
    transition: {
      duration: 0.8,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ isVisible }) => {
  const theme = useTheme();

  if (!isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      transition={{ duration: 0.2 }}
    >
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 0.5,
          p: 1.5,
          borderRadius: 2,
          bgcolor: alpha(theme.palette.secondary.main, 0.05),
          width: 'fit-content',
          maxWidth: '60px',
        }}
      >
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            variants={dotVariants}
            initial="initial"
            animate="animate"
            custom={i}
            style={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              backgroundColor: theme.palette.secondary.main,
              opacity: 0.6,
            }}
            transition={{
              delay: i * 0.15,
            }}
          />
        ))}
      </Box>
    </motion.div>
  );
}; 