import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import {
  Add as AddIcon,
  VideoCall as VideoCallIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';
import { Interview } from '@/types/api';

const mockInterviews: Interview[] = [
  {
    id: 1,
    title: 'Senior Frontend Developer',
    user_id: 1,
    status: 'scheduled',
    created_at: '2023-11-20T10:00:00Z',
    scheduled_at: '2023-11-25T14:00:00Z',
    meeting_link: 'https://meet.google.com/abc-defg-hij',
  },
  {
    id: 2,
    title: 'DevOps Engineer',
    user_id: 1,
    status: 'completed',
    created_at: '2023-11-19T09:00:00Z',
    scheduled_at: '2023-11-20T11:00:00Z',
    meeting_link: 'https://meet.google.com/xyz-uvwx-yz',
  },
  // Add more mock data as needed
];

const getStatusColor = (status: Interview['status']) => {
  switch (status) {
    case 'scheduled':
      return 'primary';
    case 'in_progress':
      return 'warning';
    case 'completed':
      return 'success';
    case 'cancelled':
      return 'error';
    default:
      return 'default';
  }
};

export default function Interviews() {
  const [interviews] = useState<Interview[]>(mockInterviews);

  return (
    <Box>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 3,
        }}
      >
        <Typography variant="h4">Interviews</Typography>
        <Button variant="contained" startIcon={<AddIcon />} sx={{ borderRadius: 2 }}>
          New Interview
        </Button>
      </Box>

      <Card>
        <CardContent sx={{ p: 0 }}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Scheduled Date</TableCell>
                  <TableCell>Created Date</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {interviews.map(interview => (
                  <TableRow key={interview.id}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography variant="body1">{interview.title}</Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={interview.status}
                        color={getStatusColor(interview.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{format(new Date(interview.scheduled_at), 'PPp')}</TableCell>
                    <TableCell>{format(new Date(interview.created_at), 'PP')}</TableCell>
                    <TableCell align="right">
                      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                        {interview.status === 'scheduled' && (
                          <IconButton
                            component="a"
                            color="primary"
                            href={interview.meeting_link || '#'}
                            target="_blank"
                          >
                            <VideoCallIcon />
                          </IconButton>
                        )}
                        <IconButton color="info">
                          <EditIcon />
                        </IconButton>
                        <IconButton color="error">
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
}
