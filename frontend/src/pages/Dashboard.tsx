import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  LinearProgress,
  IconButton,
} from '@mui/material';
import {
  VideoCall as VideoCallIcon,
  People as PeopleIcon,
  Assessment as AssessmentIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { interviews } from '@/services/api';
import { Interview } from '@/types/api';
import { format } from 'date-fns';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}

function StatCard({ title, value, icon, color }: StatCardProps) {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              p: 1,
              borderRadius: 1,
              bgcolor: `${color}.light`,
              color: `${color}.main`,
              mr: 2,
            }}
          >
            {icon}
          </Box>
          <Typography variant="h6">{title}</Typography>
        </Box>
        <Typography variant="h4">{value}</Typography>
      </CardContent>
    </Card>
  );
}

export default function Dashboard() {
  const { data: interviews, isLoading } = useQuery<Interview[]>(['interviews'], () =>
    interviews.getAll()
  );

  if (isLoading) {
    return <LinearProgress />;
  }

  const totalInterviews = interviews?.length || 0;
  const completedInterviews = interviews?.filter(i => i.status === 'completed').length || 0;
  const upcomingInterviews = interviews?.filter(i => i.status === 'scheduled').length || 0;

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Dashboard
      </Typography>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Interviews"
            value={totalInterviews}
            icon={<VideoCallIcon />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Completed"
            value={completedInterviews}
            icon={<AssessmentIcon />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Upcoming"
            value={upcomingInterviews}
            icon={<CalendarIcon />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Candidates"
            value={totalInterviews}
            icon={<PeopleIcon />}
            color="info"
          />
        </Grid>
      </Grid>

      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Upcoming Interviews
          </Typography>
          {interviews
            ?.filter(interview => interview.status === 'scheduled')
            .slice(0, 5)
            .map(interview => (
              <Box
                key={interview.id}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  py: 2,
                  borderBottom: '1px solid',
                  borderColor: 'divider',
                  '&:last-child': {
                    borderBottom: 'none',
                  },
                }}
              >
                <Box>
                  <Typography variant="subtitle1">{interview.title}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {format(new Date(interview.scheduled_at), 'PPp')}
                  </Typography>
                </Box>
                {interview.meeting_link && (
                  <IconButton
                    component="a"
                    href={interview.meeting_link}
                    target="_blank"
                    color="primary"
                  >
                    <VideoCallIcon />
                  </IconButton>
                )}
              </Box>
            ))}
        </CardContent>
      </Card>
    </Box>
  );
}
