import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Rating,
  TextField,
  Box,
  FormControlLabel,
  Switch,
  useTheme
} from '@mui/material';
import { Star as StarIcon } from '@mui/icons-material';

interface FeedbackDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (feedback: {
    rating: number;
    wasHelpful: boolean;
    comment: string;
  }) => void;
}

export const FeedbackDialog: React.FC<FeedbackDialogProps> = ({
  open,
  onClose,
  onSubmit
}) => {
  const theme = useTheme();
  const [rating, setRating] = useState<number | null>(null);
  const [wasHelpful, setWasHelpful] = useState(false);
  const [comment, setComment] = useState('');

  const handleSubmit = () => {
    if (rating !== null) {
      onSubmit({
        rating,
        wasHelpful,
        comment
      });
      handleReset();
    }
  };

  const handleReset = () => {
    setRating(null);
    setWasHelpful(false);
    setComment('');
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 2,
          p: 2
        }
      }}
    >
      <DialogTitle sx={{ textAlign: 'center' }}>
        <Typography variant="h5" component="div" gutterBottom>
          How was your experience?
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Your feedback helps us improve our responses
        </Typography>
      </DialogTitle>

      <DialogContent>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 3,
            py: 2
          }}
        >
          {/* Star Rating */}
          <Box sx={{ textAlign: 'center' }}>
            <Typography component="legend" gutterBottom>
              Rate the response quality
            </Typography>
            <Rating
              value={rating}
              onChange={(_, newValue) => setRating(newValue)}
              size="large"
              icon={<StarIcon fontSize="inherit" />}
              emptyIcon={<StarIcon fontSize="inherit" />}
              sx={{
                '& .MuiRating-iconFilled': {
                  color: theme.palette.warning.main
                }
              }}
            />
          </Box>

          {/* Helpful Switch */}
          <FormControlLabel
            control={
              <Switch
                checked={wasHelpful}
                onChange={(e) => setWasHelpful(e.target.checked)}
                color="success"
              />
            }
            label="Was this response helpful?"
          />

          {/* Comment Field */}
          <TextField
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            placeholder="Share your thoughts or suggestions (optional)"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
        </Box>
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button
          onClick={() => {
            handleReset();
            onClose();
          }}
          color="inherit"
        >
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={rating === null}
        >
          Submit Feedback
        </Button>
      </DialogActions>
    </Dialog>
  );
}; 