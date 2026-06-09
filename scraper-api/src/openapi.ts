export const openApiSpec = `
openapi: 3.0.3
info:
  title: Google Maps Scraper API
  version: 1.0.0
  description: API for managing Google Maps scraping tasks

servers:
  - url: http://localhost:9001
    description: Local server

paths:
  /api/v1/jobs:
    post:
      summary: Create a new job scraping task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - keywords
                - lang
                - zoom
                - lat
                - lon
                - fast_mode
                - radius
                - depth
                - email
                - max_time
              properties:
                name:
                  type: string
                keywords:
                  type: array
                  items:
                    type: string
                lang:
                  type: string
                zoom:
                  type: integer
                lat:
                  type: string
                lon:
                  type: string
                fast_mode:
                  type: boolean
                radius:
                  type: integer
                depth:
                  type: integer
                email:
                  type: boolean
                max_time:
                  type: integer
                proxies:
                  type: array
                  items:
                    type: string
      responses:
        '201':
          description: Job created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: string
        '422':
          description: Unprocessable entity
        '500':
          description: Internal server error

    get:
      summary: Get all jobs
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Job'
        '500':
          description: Internal server error

  /api/v1/jobs/{id}:
    get:
      summary: Get a specific job
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Job'
        '404':
          description: Job not found
        '422':
          description: Invalid ID

    delete:
      summary: Delete a specific job
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Job deleted successfully
        '422':
          description: Invalid ID
        '500':
          description: Internal server error

  /api/v1/jobs/{id}/download:
    get:
      summary: Download job results as CSV
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            text/csv:
              schema:
                type: string
                format: binary
        '404':
          description: File not found
        '422':
          description: Invalid ID
        '500':
          description: Internal server error

  /api/docs:
    get:
      summary: API Documentation (Redoc)
      responses:
        '200':
          description: Redoc HTML page
          content:
            text/html:
              schema:
                type: string

  /static/spec/spec.yaml:
    get:
      summary: OpenAPI Specification (YAML)
      responses:
        '200':
          description: OpenAPI YAML
          content:
            application/yaml:
              schema:
                type: string

components:
  schemas:
    ApiError:
      type: object
      properties:
        code:
          type: integer
        message:
          type: string

    ApiScrapeRequest:
      type: object
      properties:
        name:
          type: string
        keywords:
          type: array
          items:
            type: string
        lang:
          type: string
        zoom:
          type: integer
        lat:
          type: string
        lon:
          type: string
        fast_mode:
          type: boolean
        radius:
          type: integer
        depth:
          type: integer
        email:
          type: boolean
        max_time:
          type: integer
        proxies:
          type: array
          items:
            type: string

    ApiScrapeResponse:
      type: object
      properties:
        id:
          type: string

    Job:
      type: object
      properties:
        ID:
          type: string
        Name:
          type: string
        Date:
          type: string
          format: date-time
        Status:
          type: string
          enum: [pending, working, completed, failed]
        Data:
          $ref: '#/components/schemas/JobData'

    JobData:
      type: object
      properties:
        keywords:
          type: array
          items:
            type: string
        lang:
          type: string
        zoom:
          type: integer
        lat:
          type: string
        lon:
          type: string
        fast_mode:
          type: boolean
        radius:
          type: integer
        depth:
          type: integer
        email:
          type: boolean
        max_time:
          type: integer
        proxies:
          type: array
          items:
            type: string
        extra_reviews:
          type: boolean
`;