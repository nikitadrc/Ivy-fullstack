export type QuestionType = 'technical' | 'coding' | 'behavioral' | 'system_design' | 'resume';

export interface Message {
  id?: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
}

export interface ChatSession {
  id: number;
  questionType: QuestionType;
  chatHistory: Message[];
  createdAt: Date;
}

export interface ChatResponse {
  id: number;
  answer: string;
  context_used: string[];
  confidence_score: number;
  suggested_topics: string[];
}

export interface Feedback {
  rating: number;
  wasHelpful: boolean;
  comment?: string;
  createdAt: Date;
}

export interface WSMessage {
  type: string;
  user_id: number;
  content?: Record<string, any>;
}

export interface WSTypingIndicator extends WSMessage {
  content: {
    is_typing: boolean;
  };
} 