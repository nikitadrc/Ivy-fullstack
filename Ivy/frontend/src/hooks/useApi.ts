import { useQuery, useMutation, UseQueryOptions, UseMutationOptions } from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { ApiError } from '../types/api';
import api from '../services/api';

export function useGet<T>(
  key: string[],
  url: string,
  options?: UseQueryOptions<T, AxiosError<ApiError>>
) {
  return useQuery<T, AxiosError<ApiError>>(
    key,
    async () => {
      const { data } = await api.get<T>(url);
      return data;
    },
    options
  );
}

export function usePost<T, V>(
  url: string,
  options?: UseMutationOptions<T, AxiosError<ApiError>, V>
) {
  return useMutation<T, AxiosError<ApiError>, V>(async variables => {
    const { data } = await api.post<T>(url, variables);
    return data;
  }, options);
}

export function usePatch<T, V>(
  url: string,
  options?: UseMutationOptions<T, AxiosError<ApiError>, V>
) {
  return useMutation<T, AxiosError<ApiError>, V>(async variables => {
    const { data } = await api.patch<T>(url, variables);
    return data;
  }, options);
}

export function useDelete(
  url: string,
  options?: UseMutationOptions<void, AxiosError<ApiError>, void>
) {
  return useMutation<void, AxiosError<ApiError>, void>(async () => {
    await api.delete(url);
  }, options);
}
