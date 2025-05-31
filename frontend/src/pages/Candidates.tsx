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
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  MenuItem,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { Candidate } from '@/types/api';

const getStatusColor = (status: Candidate['status']) => {
  switch (status) {
    case 'pending':
      return 'warning';
    case 'interviewed':
      return 'info';
    case 'hired':
      return 'success';
    case 'rejected':
      return 'error';
    default:
      return 'default';
  }
};

const STATUS_OPTIONS = [
  { value: 'pending', label: 'Pending' },
  { value: 'interviewed', label: 'Interviewed' },
  { value: 'hired', label: 'Hired' },
  { value: 'rejected', label: 'Rejected' },
];

export default function Candidates() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    position: '',
    status: 'pending' as Candidate['status'],
  });

  const { data: candidates, isLoading } = useQuery<Candidate[]>(['candidates'], () =>
    fetch('/api/candidates').then(res => res.json())
  );

  const handleOpenDialog = (candidate?: Candidate) => {
    if (candidate) {
      setSelectedCandidate(candidate);
      setFormData({
        name: candidate.name,
        email: candidate.email,
        position: candidate.position,
        status: candidate.status,
      });
    } else {
      setSelectedCandidate(null);
      setFormData({
        name: '',
        email: '',
        position: '',
        status: 'pending',
      });
    }
    setIsDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setSelectedCandidate(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement create/update candidate
    handleCloseDialog();
  };

  const filteredCandidates = candidates?.filter(
    candidate =>
      candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      candidate.position.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return <LinearProgress />;
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
          Candidates
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
          sx={{ borderRadius: 2 }}
        >
          Add Candidate
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', mb: 3 }}>
            <TextField
              fullWidth
              placeholder="Search candidates..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
              }}
              sx={{ maxWidth: 500 }}
            />
          </Box>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>Position</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredCandidates?.map(candidate => (
                  <TableRow key={candidate.id}>
                    <TableCell>{candidate.name}</TableCell>
                    <TableCell>{candidate.email}</TableCell>
                    <TableCell>{candidate.position}</TableCell>
                    <TableCell>
                      <Chip
                        label={candidate.status}
                        color={getStatusColor(candidate.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{format(new Date(candidate.created_at), 'PP')}</TableCell>
                    <TableCell align="right">
                      <IconButton
                        color="info"
                        size="small"
                        onClick={() => handleOpenDialog(candidate)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton color="error" size="small">
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      <Dialog open={isDialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedCandidate ? 'Edit Candidate' : 'Add New Candidate'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                fullWidth
                label="Name"
                value={formData.name}
                onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
                required
              />
              <TextField
                fullWidth
                label="Email"
                type="email"
                value={formData.email}
                onChange={e => setFormData(prev => ({ ...prev, email: e.target.value }))}
                required
              />
              <TextField
                fullWidth
                label="Position"
                value={formData.position}
                onChange={e => setFormData(prev => ({ ...prev, position: e.target.value }))}
                required
              />
              <TextField
                select
                fullWidth
                label="Status"
                value={formData.status}
                onChange={e =>
                  setFormData(prev => ({
                    ...prev,
                    status: e.target.value as Candidate['status'],
                  }))
                }
                required
              >
                {STATUS_OPTIONS.map(option => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button type="submit" variant="contained">
              {selectedCandidate ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
}
