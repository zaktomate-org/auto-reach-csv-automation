import { Hono } from 'hono';
import { createJobHandler, listJobsHandler, getJobHandler, deleteJobHandler, downloadJobHandler } from './handlers.js';

export const routes = new Hono()
  .post('/api/v1/jobs', createJobHandler)
  .get('/api/v1/jobs', listJobsHandler)
  .get('/api/v1/jobs/:id', getJobHandler)
  .delete('/api/v1/jobs/:id', deleteJobHandler)
  .get('/api/v1/jobs/:id/download', downloadJobHandler);