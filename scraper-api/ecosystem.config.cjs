module.exports = {
  apps: [{
    name: 'scraper-api',
    script: 'src/index.ts',
    interpreter: 'bun',
    interpreter_args: 'run',
    cwd: __dirname,
    env: {
      PORT: 9001,
      HOST: '0.0.0.0',
      DATA_DIR: '../gmapsdata',
      CLI_BINARY: './bin/google-maps-scraper',
      QUEUE_FILE: '../gmapsdata/jobs.json',
      CLEANUP_THRESHOLD: 50,
      CLEANUP_COUNT: 5,
      WORKER_POLL_MS: 1000,
      DEFAULT_TIMEOUT_MS: 3600000,
    },
    max_memory_restart: '500M',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    out_file: '../logs/scraper-out.log',
    error_file: '../logs/scraper-err.log',
    merge_logs: true,
  }]
};