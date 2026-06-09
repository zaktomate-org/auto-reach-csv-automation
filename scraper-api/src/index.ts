import { Hono } from 'hono';
import { routes } from './routes.js';
import { startWorker } from './worker.js';
import { config } from './config.js';
import { openApiSpec } from './openapi.js';

const app = new Hono();

app.route('/', routes);

app.get('/static/spec/spec.yaml', (c) => {
  return c.text(openApiSpec.trim(), 200, { 'Content-Type': 'application/yaml' });
});

app.get('/api/docs', (c) => {
  const html = `<!DOCTYPE html>
<html>
  <head>
    <title>API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
  </head>
  <body>
    <redoc spec-url="/static/spec/spec.yaml"></redoc>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
  </body>
</html>`;
  return c.html(html);
});

async function main() {
  console.log(`[server] Starting on ${config.host}:${config.port}`);
  console.log(`[server] Data dir: ${config.dataDir}`);
  console.log(`[server] CLI binary: ${config.cliBinary}`);
  console.log(`[server] Queue file: ${config.queueFile}`);

  startWorker().catch(err => {
    console.error('[worker] Fatal error:', err);
    process.exit(1);
  });

  Bun.serve({
    fetch: app.fetch,
    port: config.port,
    hostname: config.host,
  });

  console.log(`[server] Listening on http://${config.host}:${config.port}`);
}

main().catch(err => {
  console.error('[server] Fatal error:', err);
  process.exit(1);
});