import { getNextPending, updateStatus, resetWorkingJobs } from './queue.js';
import { executeCLI } from './cli.js';
import { cleanupIfNeeded } from './cleanup.js';
import { config } from './config.js';

function sleep(ms: number): Promise<void> {
  return new Promise(r => setTimeout(r, ms));
}

export async function startWorker(): Promise<void> {
  const resetCount = await resetWorkingJobs();
  if (resetCount > 0) {
    console.log(`[worker] Reset ${resetCount} stuck working jobs to pending`);
  }
  console.log('[worker] Started');
  while (true) {
    const job = await getNextPending();
    if (!job) {
      await sleep(config.workerPollMs);
      continue;
    }

    console.log(`[worker] Processing job ${job.ID}`);
    await updateStatus(job.ID, 'working');

    const result = await executeCLI(job);

    if (result.ok) {
      await updateStatus(job.ID, 'completed');
      console.log(`[worker] Job ${job.ID} completed`);
    } else {
      await updateStatus(job.ID, 'failed');
      console.error(`[worker] Job ${job.ID} failed: ${result.error}`);
    }

    await cleanupIfNeeded();
  }
}