import React from 'react';
import {
  ToggleButtonGroup,
  ToggleButton,
  Box,
  useTheme,
  alpha
} from '@mui/material';
import {
  Code as CodeIcon,
  Psychology as TechnicalIcon,
  Architecture as SystemDesignIcon,
  Person as BehavioralIcon,
  Description as ResumeIcon
} from '@mui/icons-material';
import { QuestionType } from '../types/chat';

interface QuestionTypeSelectorProps {
  value: QuestionType;
  onChange: (type: QuestionType) => void;
}

interface QuestionTypeOption {
  value: QuestionType;
  label: string;
  icon: React.ReactElement;
}

const questionTypes: QuestionTypeOption[] = [
  {
    value: 'technical',
    label: 'Technical',
    icon: <TechnicalIcon />
  },
  {
    value: 'coding',
    label: 'Coding',
    icon: <CodeIcon />
  },
  {
    value: 'behavioral',
    label: 'Behavioral',
    icon: <BehavioralIcon />
  },
  {
    value: 'system_design',
    label: 'System Design',
    icon: <SystemDesignIcon />
  },
  {
    value: 'resume',
    label: 'Resume',
    icon: <ResumeIcon />
  }
];

export const QuestionTypeSelector: React.FC<QuestionTypeSelectorProps> = ({
  value,
  onChange
}) => {
  const theme = useTheme();

  return (
    <Box sx={{ mb: 2 }}>
      <ToggleButtonGroup
        value={value}
        exclusive
        onChange={(_, newValue) => {
          if (newValue !== null) {
            onChange(newValue);
          }
        }}
        aria-label="question type"
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 1,
          '& .MuiToggleButton-root': {
            flex: '1 1 auto',
            minWidth: 120,
            borderRadius: 2,
            border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
            '&.Mui-selected': {
              bgcolor: alpha(theme.palette.primary.main, 0.1),
              '&:hover': {
                bgcolor: alpha(theme.palette.primary.main, 0.2)
              }
            }
          }
        }}
      >
        {questionTypes.map((type) => (
          <ToggleButton
            key={type.value}
            value={type.value}
            aria-label={type.label}
          >
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 0.5,
                py: 0.5
              }}
            >
              {React.cloneElement(type.icon, {
                sx: { color: theme.palette.primary.main }
              })}
              {type.label}
            </Box>
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
    </Box>
  );
}; 