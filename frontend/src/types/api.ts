// User types
export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  password: string;
  name: string;
}

// Authentication types
export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

// Interview types
export interface Interview {
  id: number;
  title: string;
  user_id: number;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  created_at: string;
  scheduled_at: string;
  meeting_link?: string;
  candidate_name?: string;
  position?: string;
  notes?: string;
}

export interface InterviewCreate {
  title: string;
  scheduled_at: string;
  candidate_name?: string;
  position?: string;
}

export interface InterviewUpdate {
  title?: string;
  status?: Interview['status'];
  scheduled_at?: string;
  meeting_link?: string;
  notes?: string;
}

// Question types
export interface Question {
  id: number;
  interview_id: number;
  content: string;
  type: 'technical' | 'behavioral' | 'coding';
  created_at: string;
}

// Response types
export interface Response {
  id: number;
  question_id: number;
  content: string;
  created_at: string;
  feedback?: string;
  score?: number;
}

// File types
export interface File {
  id: number;
  interview_id: number;
  filename: string;
  file_type: string;
  s3_key: string;
  created_at: string;
}

// API Error type
export interface ApiError {
  detail: string;
  code?: string;
  status?: number;
}

export interface Candidate {
  id: number;
  name: string;
  email: string;
  position: string;
  status: 'pending' | 'interviewed' | 'hired' | 'rejected';
  created_at: string;
  updated_at: string;
}

export interface Analytics {
  total_interviews: number;
  completed_interviews: number;
  upcoming_interviews: number;
  average_duration: number;
  interview_by_status: Record<Interview['status'], number>;
  interviews_by_month: Array<{
    month: string;
    count: number;
  }>;
}
