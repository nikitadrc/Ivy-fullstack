import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  LinearProgress,
  useTheme,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { interviews } from '@/services/api';
import { Interview } from '@/types/api';
import { format, parseISO, startOfMonth, endOfMonth } from 'date-fns';

const COLORS = ['#2563eb', '#16a34a', '#dc2626', '#ca8a04'];

const STATUS_LABELS = {
  scheduled: 'Scheduled',
  in_progress: 'In Progress',
  completed: 'Completed',
  cancelled: 'Cancelled',
};

export default function Analytics() {
  const theme = useTheme();
  const { data: interviewsData, isLoading } = useQuery<Interview[]>(['interviews'], () =>
    interviews.getAll()
  );

  if (isLoading) {
    return <LinearProgress />;
  }

  const getStatusCount = (status: Interview['status']) =>
    interviewsData?.filter(interview => interview.status === status).length || 0;

  const statusData = Object.entries(STATUS_LABELS).map(([status, label]) => ({
    name: label,
    value: getStatusCount(status as Interview['status']),
  }));

  const monthlyData = interviewsData
    ? Array.from({ length: 6 }, (_, i) => {
        const date = new Date();
        date.setMonth(date.getMonth() - i);
        const start = startOfMonth(date);
        const end = endOfMonth(date);

        return {
          name: format(date, 'MMM'),
          total: interviewsData.filter(
            interview =>
              parseISO(interview.scheduled_at) >= start &&
              parseISO(interview.scheduled_at) <= end
          ).length,
        };
      })
    : [];

  const totalInterviews = interviewsData?.length || 0;
  const completedInterviews = getStatusCount('completed');
  const completionRate = totalInterviews
    ? Math.round((completedInterviews / totalInterviews) * 100)
    : 0;

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 4 }}>
        Analytics
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Monthly Interviews
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={monthlyData.reverse()}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar
                      dataKey="total"
                      fill={theme.palette.primary.main}
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Interview Status Distribution
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={statusData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {statusData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
              <Box sx={{ mt: 2 }}>
                {statusData.map((item, index) => (
                  <Box
                    key={item.name}
                    sx={{ display: 'flex', alignItems: 'center', mb: 1 }}
                  >
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: '50%',
                        bgcolor: COLORS[index % COLORS.length],
                        mr: 1,
                      }}
                    />
                    <Typography variant="body2" sx={{ flexGrow: 1 }}>
                      {item.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {item.value}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Key Metrics
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={4}>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Total Interviews
                    </Typography>
                    <Typography variant="h4">{totalInterviews}</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Completed Interviews
                    </Typography>
                    <Typography variant="h4">{completedInterviews}</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Completion Rate
                    </Typography>
                    <Typography variant="h4">{completionRate}%</Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
