import { Context } from 'hono';
import { randomUUID } from 'crypto';
import { createJob, readJobs, getById, deleteById, updateStatus } from './queue.js';
import { deleteJobFiles } from './cleanup.js';
import { Job, ApiScrapeRequest, ApiScrapeResponse, ApiError } from './models.js';
import { config } from './config.js';

export async function createJobHandler(c: Context): Promise<Response> {
  const body = await c.req.json<ApiScrapeRequest>();
  const now = new Date().toISOString();
  const job: Job = {
    ID: randomUUID(),
    Name: body.name,
    Date: now,
    Status: 'pending',
    Data: {
      keywords: body.keywords,
      lang: body.lang,
      zoom: body.zoom,
      lat: body.lat,
      lon: body.lon,
      fast_mode: body.fast_mode,
      radius: body.radius,
      depth: body.depth,
      email: body.email,
      max_time: body.max_time,
      proxies: body.proxies || null,
      extra_reviews: false,
    },
  };
  await createJob(job);
  const response: ApiScrapeResponse = { id: job.ID };
  return c.json(response, 201);
}

export async function listJobsHandler(c: Context): Promise<Response> {
  const jobs = await readJobs();
  return c.json(jobs);
}

export async function getJobHandler(c: Context): Promise<Response> {
  const id = c.req.param('id');
  const job = await getById(id);
  if (!job) {
    const error: ApiError = { code: 404, message: 'Job not found' };
    return c.json(error, 404);
  }
  return c.json(job);
}

export async function deleteJobHandler(c: Context): Promise<Response> {
  const id = c.req.param('id');
  const job = await getById(id);
  if (!job) {
    const error: ApiError = { code: 404, message: 'Job not found' };
    return c.json(error, 404);
  }
  await deleteById(id);
  await deleteJobFiles(id);
  return c.body(null, 200);
}

export async function downloadJobHandler(c: Context): Promise<Response> {
  const id = c.req.param('id');
  const job = await getById(id);
  if (!job) {
    return c.text('Job not found', 404);
  }
  if (job.Status !== 'completed') {
    return c.text('Job not completed', 400);
  }
  const file = Bun.file(`${config.dataDir}/${id}.csv`);
  if (!(await file.exists())) {
    return c.text('File not found', 404);
  }
  return new Response(file.stream(), {
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': `attachment; filename="${id}.csv"`,
    },
  });
}