import { useQuery } from '@tanstack/react-query';
import { ChatHistoryResponse } from '../types/api';

export const useChatHistory = (userId: number) => {
  return useQuery<ChatHistoryResponse>({
    queryKey: ['chatHistory', userId],
    queryFn: async () => {
      const response = await fetch(`/api/chat/${userId}/history`);
      if (!response.ok) {
        throw new Error('Failed to fetch chat history');
      }
      return response.json();
    },
    staleTime: 1000 * 60 * 5, // Consider data fresh for 5 minutes
    cacheTime: 1000 * 60 * 30, // Keep data in cache for 30 minutes
  });
}; 