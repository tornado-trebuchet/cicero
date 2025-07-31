// Export all models and enums
export * from './enums';
export * from './common.models';
export * from './context.models';
export * from './text.models';

// Utility types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface ErrorResponse {
  error: string;
  message: string;
  status_code: number;
}
