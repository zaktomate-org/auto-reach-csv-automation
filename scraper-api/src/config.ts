export const config = {
  port: parseInt(Bun.env.PORT || '9001', 10),
  host: Bun.env.HOST || '0.0.0.0',
  dataDir: Bun.env.DATA_DIR || '../gmapsdata',
  cliBinary: Bun.env.CLI_BINARY || './bin/google-maps-scraper',
  queueFile: Bun.env.QUEUE_FILE || '../gmapsdata/jobs.json',
  cleanupThreshold: parseInt(Bun.env.CLEANUP_THRESHOLD || '50', 10),
  cleanupCount: parseInt(Bun.env.CLEANUP_COUNT || '5', 10),
  workerPollMs: parseInt(Bun.env.WORKER_POLL_MS || '1000', 10),
  defaultTimeoutMs: parseInt(Bun.env.DEFAULT_TIMEOUT_MS || '3600000', 10),
} as const;