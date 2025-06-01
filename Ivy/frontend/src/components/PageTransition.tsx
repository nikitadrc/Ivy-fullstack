import React from 'react';
import { motion, Variants } from 'framer-motion';

interface PageTransitionProps {
  children: React.ReactNode;
}

const pageVariants: Variants = {
  initial: {
    opacity: 0,
    scale: 0.98,
    y: 20,
  },
  animate: {
    opacity: 1,
    scale: 1,
    y: 0,
  },
  exit: {
    opacity: 0,
    scale: 0.98,
    y: -20,
  },
};

const pageTransition = {
  type: 'spring',
  stiffness: 300,
  damping: 30,
};

export default function PageTransition({ children }: PageTransitionProps) {
  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageVariants}
      transition={pageTransition}
      style={{
        width: '100%',
        height: '100%',
      }}
    >
      {children}
    </motion.div>
  );
} 