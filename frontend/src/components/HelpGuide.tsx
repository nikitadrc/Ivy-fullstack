import React, { useState } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Stepper,
  Step,
  StepLabel,
  StepContent,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Help as HelpIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const faqs = [
  {
    question: 'How do I schedule an interview?',
    answer: 'Navigate to the Calendar page and click on any date to schedule a new interview. Fill in the required details like candidate name, position, and time.',
  },
  {
    question: 'Can I track interview progress?',
    answer: 'Yes! The Dashboard shows your upcoming interviews and their status. The Analytics page provides detailed insights into your interview process.',
  },
  {
    question: 'How do I manage candidates?',
    answer: 'Use the Candidates page to add, edit, or track candidates. You can update their status, add notes, and view their interview history.',
  },
  {
    question: 'How do I customize notifications?',
    answer: 'Go to Settings > Preferences to customize email and desktop notifications for interview reminders and updates.',
  },
  {
    question: 'Can I export interview data?',
    answer: 'Yes, you can export interview data and analytics from the Analytics page using the export button in the top right corner.',
  },
];

const tourSteps = [
  {
    label: 'Dashboard Overview',
    description: 'Get a quick overview of your upcoming interviews, recent activities, and key metrics.',
  },
  {
    label: 'Calendar Management',
    description: 'Schedule and manage interviews with an intuitive calendar interface.',
  },
  {
    label: 'Analytics & Insights',
    description: 'Track your interview process with detailed analytics and visualizations.',
  },
  {
    label: 'Candidate Management',
    description: 'Manage candidate profiles, track their progress, and maintain interview records.',
  },
  {
    label: 'Settings & Customization',
    description: 'Customize your experience with personalized settings and preferences.',
  },
];

const MotionDialog = motion(Dialog);

export default function HelpGuide() {
  const [open, setOpen] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [showTour, setShowTour] = useState(false);

  const handleNext = () => {
    setActiveStep(prevStep => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep(prevStep => prevStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setShowTour(false);
    setActiveStep(0);
  };

  return (
    <>
      <IconButton
        onClick={handleOpen}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          bgcolor: 'primary.main',
          color: 'white',
          '&:hover': {
            bgcolor: 'primary.dark',
          },
          zIndex: 1300,
        }}
      >
        <HelpIcon />
      </IconButton>

      <Dialog
        open={open}
        onClose={handleClose}
        maxWidth="md"
        fullWidth
        sx={{
          '& .MuiDialog-paper': {
            bgcolor: 'background.paper',
          },
        }}
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h5">Help & Guide</Typography>
            <IconButton onClick={handleClose}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>

        <DialogContent>
          {!showTour ? (
            <Box>
              <Typography variant="h6" gutterBottom>
                Frequently Asked Questions
              </Typography>
              {faqs.map((faq, index) => (
                <Accordion key={index}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>{faq.question}</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography color="text.secondary">{faq.answer}</Typography>
                  </AccordionDetails>
                </Accordion>
              ))}
            </Box>
          ) : (
            <Box sx={{ maxWidth: 400, mx: 'auto' }}>
              <Stepper activeStep={activeStep} orientation="vertical">
                {tourSteps.map((step, index) => (
                  <Step key={step.label}>
                    <StepLabel>{step.label}</StepLabel>
                    <StepContent>
                      <Typography>{step.description}</Typography>
                      <Box sx={{ mb: 2 }}>
                        <div>
                          <Button
                            variant="contained"
                            onClick={handleNext}
                            sx={{ mt: 1, mr: 1 }}
                          >
                            {index === tourSteps.length - 1 ? 'Finish' : 'Continue'}
                          </Button>
                          <Button
                            disabled={index === 0}
                            onClick={handleBack}
                            sx={{ mt: 1, mr: 1 }}
                          >
                            Back
                          </Button>
                        </div>
                      </Box>
                    </StepContent>
                  </Step>
                ))}
              </Stepper>
              {activeStep === tourSteps.length && (
                <Box sx={{ p: 3 }}>
                  <Typography>All steps completed!</Typography>
                  <Button onClick={handleReset} sx={{ mt: 1, mr: 1 }}>
                    Reset Tour
                  </Button>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={() => setShowTour(!showTour)}>
            {showTour ? 'Show FAQs' : 'Take a Tour'}
          </Button>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  );
} 