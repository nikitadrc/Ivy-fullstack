import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Grid,
  Chip,
  useTheme,
  Stack
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  LocalFireDepartment as StreakIcon,
  Star as StarIcon
} from '@mui/icons-material';

interface TopicProgress {
  topic: string;
  progress: number;
  priority: 'High' | 'Medium' | 'Low';
}

interface ProgressTrackerProps {
  overallProgress: number;
  topicProgress: Record<string, number>;
  recommendations: {
    topic: string;
    current_progress: number;
    priority: 'High' | 'Medium' | 'Low';
  }[];
  streak: number;
}

const getPriorityColor = (priority: string) => {
  switch (priority.toLowerCase()) {
    case 'high':
      return 'error';
    case 'medium':
      return 'warning';
    case 'low':
      return 'success';
    default:
      return 'default';
  }
};

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({
  overallProgress,
  topicProgress,
  recommendations,
  streak
}) => {
  const theme = useTheme();

  return (
    <Box sx={{ py: 3 }}>
      <Grid container spacing={3}>
        {/* Overall Progress Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUpIcon sx={{ mr: 1, color: theme.palette.primary.main }} />
                <Typography variant="h6">Overall Progress</Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <Box sx={{ flexGrow: 1, mr: 1 }}>
                  <LinearProgress
                    variant="determinate"
                    value={overallProgress}
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {Math.round(overallProgress)}%
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Streak Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <StreakIcon sx={{ mr: 1, color: theme.palette.warning.main }} />
                <Typography variant="h6">Study Streak</Typography>
              </Box>
              <Typography variant="h3" sx={{ textAlign: 'center', color: theme.palette.warning.main }}>
                {streak} Days
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Recommendations Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <StarIcon sx={{ mr: 1, color: theme.palette.info.main }} />
                <Typography variant="h6">Recommended Topics</Typography>
              </Box>
              <Stack spacing={1}>
                {recommendations.map((rec) => (
                  <Box
                    key={rec.topic}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <Typography variant="body2">{rec.topic}</Typography>
                    <Chip
                      label={rec.priority}
                      size="small"
                      color={getPriorityColor(rec.priority) as any}
                    />
                  </Box>
                ))}
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Topic Progress Cards */}
        {Object.entries(topicProgress).map(([topic, progress]) => (
          <Grid item xs={12} sm={6} md={4} key={topic}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {topic}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Box sx={{ flexGrow: 1, mr: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={progress}
                      sx={{
                        height: 8,
                        borderRadius: 4,
                        backgroundColor: alpha(theme.palette.primary.main, 0.1)
                      }}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {Math.round(progress)}%
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}; 