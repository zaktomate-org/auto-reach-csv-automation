import { Job } from './models.js';
import { config } from './config.js';
import { existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import { unlink } from 'fs/promises';

const QUEUE_FILE = config.queueFile;
const LOCK_FILE = `${QUEUE_FILE}.lock`;

function ensureDir(): void {
  const dir = dirname(QUEUE_FILE);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

async function acquireLock(): Promise<void> {
  while (true) {
    try {
      await Bun.write(LOCK_FILE, String(process.pid), { createNew: true });
      return;
    } catch {
      await new Promise(r => setTimeout(r, 10));
    }
  }
}

async function releaseLock(): Promise<void> {
  try {
    await unlink(LOCK_FILE);
  } catch {}
}

async function withLock<T>(fn: () => Promise<T>): Promise<T> {
  await acquireLock();
  try {
    return await fn();
  } finally {
    await releaseLock();
  }
}

export async function readJobs(): Promise<Job[]> {
  ensureDir();
  const file = Bun.file(QUEUE_FILE);
  if (!(await file.exists())) {
    return [];
  }
  try {
    const text = await file.text();
    if (!text.trim()) return [];
    return JSON.parse(text) as Job[];
  } catch {
    return [];
  }
}

export async function writeJobs(jobs: Job[]): Promise<void> {
  ensureDir();
  const tmp = `${QUEUE_FILE}.tmp`;
  await Bun.write(tmp, JSON.stringify(jobs, null, 2));
  await Bun.write(QUEUE_FILE, JSON.stringify(jobs, null, 2));
  try { await Bun.file(tmp).delete(); } catch {}
}

export async function getNextPending(): Promise<Job | null> {
  return withLock(async () => {
    const jobs = await readJobs();
    const pending = jobs.filter(j => j.Status === 'pending');
    if (pending.length === 0) return null;
    pending.sort((a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime());
    return pending[0];
  });
}

export async function updateStatus(id: string, status: Job['Status']): Promise<boolean> {
  return withLock(async () => {
    const jobs = await readJobs();
    const idx = jobs.findIndex(j => j.ID === id);
    if (idx === -1) return false;
    jobs[idx].Status = status;
    await writeJobs(jobs);
    return true;
  });
}

export async function getById(id: string): Promise<Job | null> {
  const jobs = await readJobs();
  return jobs.find(j => j.ID === id) || null;
}

export async function deleteById(id: string): Promise<boolean> {
  return withLock(async () => {
    const jobs = await readJobs();
    const idx = jobs.findIndex(j => j.ID === id);
    if (idx === -1) return false;
    jobs.splice(idx, 1);
    await writeJobs(jobs);
    return true;
  });
}

export async function createJob(job: Job): Promise<void> {
  await withLock(async () => {
    const jobs = await readJobs();
    jobs.push(job);
    await writeJobs(jobs);
  });
}

export async function cleanupOldJobs(): Promise<number> {
  return withLock(async () => {
    const jobs = await readJobs();
    if (jobs.length <= config.cleanupThreshold) return 0;
    const eligible = jobs
      .filter(j => j.Status === 'completed' || j.Status === 'failed')
      .sort((a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime())
      .slice(0, config.cleanupCount);
    if (eligible.length === 0) return 0;
    const ids = new Set(eligible.map(j => j.ID));
    const remaining = jobs.filter(j => !ids.has(j.ID));
    await writeJobs(remaining);
    return eligible.length;
  });
}

export async function resetWorkingJobs(): Promise<number> {
  return withLock(async () => {
    const jobs = await readJobs();
    let count = 0;
    for (const job of jobs) {
      if (job.Status === 'working') {
        job.Status = 'pending';
        count++;
      }
    }
    if (count > 0) {
      await writeJobs(jobs);
    }
    return count;
  });
}