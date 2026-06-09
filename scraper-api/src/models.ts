export type JobStatus = 'pending' | 'working' | 'completed' | 'failed';

export interface JobData {
  keywords: string[];
  lang: string;
  zoom: number;
  lat: string;
  lon: string;
  fast_mode: boolean;
  radius: number;
  depth: number;
  email: boolean;
  max_time: number;
  proxies: string[] | null;
  extra_reviews: boolean;
}

export interface Job {
  ID: string;
  Name: string;
  Date: string;
  Status: JobStatus;
  Data: JobData;
}

export interface ApiScrapeRequest {
  name: string;
  keywords: string[];
  lang: string;
  zoom: number;
  lat: string;
  lon: string;
  fast_mode: boolean;
  radius: number;
  depth: number;
  email: boolean;
  max_time: number;
  proxies?: string[];
}

export interface ApiScrapeResponse {
  id: string;
}

export interface ApiError {
  code: number;
  message: string;
}