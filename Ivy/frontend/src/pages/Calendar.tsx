import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay } from 'date-fns';
import { interviews } from '@/services/api';
import { Interview } from '@/types/api';

export default function Calendar() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newInterview, setNewInterview] = useState({
    title: '',
    candidateName: '',
    position: '',
  });

  const queryClient = useQueryClient();
  const { data: interviewsData } = useQuery<Interview[]>(['interviews'], () =>
    interviews.getAll()
  );

  const createInterviewMutation = useMutation(
    (data: { title: string; scheduled_at: string }) => interviews.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['interviews']);
        handleCloseDialog();
      },
    }
  );

  const handlePreviousMonth = () => {
    setCurrentDate(prev => new Date(prev.getFullYear(), prev.getMonth() - 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(prev => new Date(prev.getFullYear(), prev.getMonth() + 1));
  };

  const handleDateClick = (date: Date) => {
    setSelectedDate(date);
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setSelectedDate(null);
    setNewInterview({ title: '', candidateName: '', position: '' });
  };

  const handleCreateInterview = () => {
    if (selectedDate && newInterview.title) {
      createInterviewMutation.mutate({
        title: newInterview.title,
        scheduled_at: selectedDate.toISOString(),
      });
    }
  };

  const days = eachDayOfInterval({
    start: startOfMonth(currentDate),
    end: endOfMonth(currentDate),
  });

  const getDayInterviews = (date: Date) =>
    interviewsData?.filter(interview =>
      isSameDay(new Date(interview.scheduled_at), date)
    ) || [];

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
          Calendar
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton onClick={handlePreviousMonth}>
            <ChevronLeftIcon />
          </IconButton>
          <Typography variant="h6" sx={{ mx: 2 }}>
            {format(currentDate, 'MMMM yyyy')}
          </Typography>
          <IconButton onClick={handleNextMonth}>
            <ChevronRightIcon />
          </IconButton>
        </Box>
      </Box>

      <Card>
        <CardContent>
          <Grid container spacing={2}>
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <Grid key={day} item xs>
                <Typography
                  variant="subtitle2"
                  align="center"
                  sx={{ color: 'text.secondary', fontWeight: 500 }}
                >
                  {day}
                </Typography>
              </Grid>
            ))}
            {Array.from({ length: startOfMonth(currentDate).getDay() }).map((_, index) => (
              <Grid key={`empty-${index}`} item xs>
                <Box sx={{ pt: '100%' }} />
              </Grid>
            ))}
            {days.map(day => {
              const dayInterviews = getDayInterviews(day);
              return (
                <Grid key={day.toString()} item xs>
                  <Box
                    onClick={() => handleDateClick(day)}
                    sx={{
                      position: 'relative',
                      pt: '100%',
                      border: '1px solid',
                      borderColor: 'divider',
                      borderRadius: 1,
                      cursor: 'pointer',
                      '&:hover': {
                        bgcolor: 'action.hover',
                      },
                    }}
                  >
                    <Box
                      sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        p: 1,
                      }}
                    >
                      <Typography
                        align="right"
                        sx={{
                          fontWeight: isSameDay(day, new Date()) ? 600 : 400,
                          color: isSameDay(day, new Date())
                            ? 'primary.main'
                            : 'text.primary',
                        }}
                      >
                        {format(day, 'd')}
                      </Typography>
                      {dayInterviews.length > 0 && (
                        <Box
                          sx={{
                            mt: 1,
                            height: 6,
                            width: 6,
                            borderRadius: '50%',
                            bgcolor: 'primary.main',
                          }}
                        />
                      )}
                    </Box>
                  </Box>
                </Grid>
              );
            })}
          </Grid>
        </CardContent>
      </Card>

      <Dialog open={isDialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Schedule Interview</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Date: {selectedDate && format(selectedDate, 'PP')}
            </Typography>
            <TextField
              fullWidth
              label="Interview Title"
              value={newInterview.title}
              onChange={e => setNewInterview(prev => ({ ...prev, title: e.target.value }))}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Candidate Name"
              value={newInterview.candidateName}
              onChange={e =>
                setNewInterview(prev => ({ ...prev, candidateName: e.target.value }))
              }
              margin="normal"
            />
            <TextField
              fullWidth
              label="Position"
              value={newInterview.position}
              onChange={e => setNewInterview(prev => ({ ...prev, position: e.target.value }))}
              margin="normal"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleCreateInterview}
            disabled={!newInterview.title}
          >
            Schedule
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
