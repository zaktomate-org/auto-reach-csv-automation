import { Job } from './models.js';
import { config } from './config.js';
import { tmpdir } from 'os';
import { join } from 'path';
import { randomUUID } from 'crypto';

async function writeKeywordsTemp(keywords: string[]): Promise<string> {
  const file = join(tmpdir(), `keywords-${randomUUID()}.txt`);
  await Bun.write(file, keywords.join('\n'));
  return file;
}

async function buildArgs(job: Job): Promise<string[]> {
  const inputFile = job.Data.keywords.length > 0
    ? await writeKeywordsTemp(job.Data.keywords)
    : '/dev/null';

  const args = [
    '-input', inputFile,
    '-results', `${config.dataDir}/${job.ID}.csv`,
    '-lang', job.Data.lang,
    '-zoom', String(job.Data.zoom),
    '-geo', `${job.Data.lat},${job.Data.lon}`,
    '-depth', String(job.Data.depth),
    '-radius', String(job.Data.radius),
    '-exit-on-inactivity', `${job.Data.max_time}s`,
  ];

  if (job.Data.fast_mode) args.push('-fast-mode');
  if (job.Data.email) args.push('-email');
  if (job.Data.extra_reviews) args.push('-extra-reviews');
  if (job.Data.proxies && job.Data.proxies.length > 0) {
    args.push('-proxies', job.Data.proxies.join(','));
  }

  return args;
}

async function readableStreamToString(stream: ReadableStream<Uint8Array>): Promise<string> {
  const reader = stream.getReader();
  let result = '';
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      result += new TextDecoder().decode(value);
    }
  } finally {
    reader.releaseLock();
  }
  return result;
}

export async function executeCLI(job: Job): Promise<{ ok: boolean; error?: string }> {
  const args = await buildArgs(job);
  const proc = Bun.spawn([config.cliBinary, ...args], {
    stdout: 'pipe',
    stderr: 'pipe',
    timeout: job.Data.max_time * 1000 || config.defaultTimeoutMs,
  });

  const [, stderr] = await Promise.all([
    readableStreamToString(proc.stdout),
    readableStreamToString(proc.stderr),
  ]);

  const exitCode = await proc.exited;
  return exitCode === 0 ? { ok: true } : { ok: false, error: stderr || `Exit code: ${exitCode}` };
}