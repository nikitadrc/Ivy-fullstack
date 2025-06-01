import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  useTheme,
  alpha,
  VisuallyHidden
} from '@mui/material';
import {
  Code as FrontendIcon,
  Storage as BackendIcon,
  DeveloperBoard as FullstackIcon,
  Analytics as DataScienceIcon,
  Cloud as DevOpsIcon,
  Psychology as AIMLIcon,
  BugReport as QAIcon
} from '@mui/icons-material';

export type Role = 'frontend' | 'backend' | 'fullstack' | 'data_scientist' | 'devops' | 'ai_ml' | 'qa';

interface RoleSelectorProps {
  selectedRole: Role | null;
  onRoleSelect: (role: Role) => void;
}

interface RoleCard {
  role: Role;
  title: string;
  description: string;
  icon: React.ReactElement;
}

const roleCards: RoleCard[] = [
  {
    role: 'frontend',
    title: 'Frontend Engineer',
    description: 'Specialize in building user interfaces and client-side applications',
    icon: <FrontendIcon />
  },
  {
    role: 'backend',
    title: 'Backend Engineer',
    description: 'Focus on server-side logic and database management',
    icon: <BackendIcon />
  },
  {
    role: 'fullstack',
    title: 'Full-stack Engineer',
    description: 'Master both frontend and backend development',
    icon: <FullstackIcon />
  },
  {
    role: 'data_scientist',
    title: 'Data Scientist',
    description: 'Analyze data and build machine learning models',
    icon: <DataScienceIcon />
  },
  {
    role: 'devops',
    title: 'DevOps Engineer',
    description: 'Manage infrastructure and deployment pipelines',
    icon: <DevOpsIcon />
  },
  {
    role: 'ai_ml',
    title: 'AI/ML Engineer',
    description: 'Build and deploy artificial intelligence solutions',
    icon: <AIMLIcon />
  },
  {
    role: 'qa',
    title: 'QA Engineer',
    description: 'Ensure software quality through testing',
    icon: <QAIcon />
  }
];

export const RoleSelector: React.FC<RoleSelectorProps> = ({
  selectedRole,
  onRoleSelect
}) => {
  const theme = useTheme();

  const handleKeyPress = (event: React.KeyboardEvent, role: Role) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onRoleSelect(role);
    }
  };

  return (
    <Box 
      sx={{ py: 4 }}
      role="region"
      aria-label="Role Selection"
    >
      <Typography variant="h4" align="center" gutterBottom>
        Choose Your Interview Role
      </Typography>
      <Typography variant="body1" align="center" sx={{ mb: 4 }}>
        Select the role you're preparing for to get personalized interview practice
      </Typography>
      
      <Grid 
        container 
        spacing={3}
        role="radiogroup"
        aria-label="Interview roles"
      >
        {roleCards.map((card) => (
          <Grid item xs={12} sm={6} md={4} key={card.role}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                backgroundColor:
                  selectedRole === card.role
                    ? alpha(theme.palette.primary.main, 0.1)
                    : 'background.paper',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: theme.shadows[4]
                },
                '&:focus-within': {
                  outline: `2px solid ${theme.palette.primary.main}`,
                  outlineOffset: '2px'
                }
              }}
              onClick={() => onRoleSelect(card.role)}
              onKeyPress={(e) => handleKeyPress(e, card.role)}
              tabIndex={0}
              role="radio"
              aria-checked={selectedRole === card.role}
              aria-label={`${card.title}: ${card.description}`}
            >
              <CardContent>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    mb: 2
                  }}
                >
                  {React.cloneElement(card.icon, {
                    sx: {
                      fontSize: 48,
                      color: theme.palette.primary.main
                    },
                    role: "img",
                    "aria-hidden": "true"
                  })}
                </Box>
                <Typography
                  gutterBottom
                  variant="h6"
                  component="h2"
                  sx={{ fontWeight: 'bold' }}
                >
                  {card.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {card.description}
                </Typography>
              </CardContent>
              <Button
                variant={selectedRole === card.role ? "contained" : "outlined"}
                sx={{ mx: 2, mb: 2 }}
                onClick={() => onRoleSelect(card.role)}
                aria-hidden="true"
                tabIndex={-1}
              >
                {selectedRole === card.role ? 'Selected' : 'Select Role'}
              </Button>
              <VisuallyHidden>
                {selectedRole === card.role ? 'Selected' : 'Not selected'}
              </VisuallyHidden>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}; 