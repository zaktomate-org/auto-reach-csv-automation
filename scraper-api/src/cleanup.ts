import { cleanupOldJobs } from './queue.js';
import { config } from './config.js';
import { unlink } from 'fs/promises';

export async function cleanupIfNeeded(): Promise<number> {
  const deletedCount = await cleanupOldJobs();
  if (deletedCount > 0) {
    console.log(`[cleanup] Removed ${deletedCount} old jobs`);
  }
  return deletedCount;
}

export async function deleteJobFiles(jobId: string): Promise<void> {
  const csvPath = `${config.dataDir}/${jobId}.csv`;
  try {
    await unlink(csvPath);
  } catch {}
}