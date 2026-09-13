# CloudOps Incident Intelligence API

A FastAPI + PostgreSQL backend project for managing cloud services, incidents, incident reports, and rule-based incident intelligence.

## What this project does

This API allows users to:

- manage cloud services
- create and track incidents
- resolve incidents
- view full incident details with service information
- generate severity and status reports
- generate service risk reports
- get rule-based incident summaries with recommended actions

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Pydantic
- psycopg2
- python-dotenv
- Uvicorn
- Docker
- Docker Compose

## Project Structure

```text
CLOUDOPS_INCIDENT_INTELLIGENCE_API/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── services.py
│   └── main.py
├── .env
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Environment Variables

Create a `.env` file in the root folder:

```env
DB_NAME=cloudops_incident_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

For local Python execution, `DB_HOST=localhost`.

For Docker Compose execution, the API container uses:

```env
DB_HOST=postgres
```

This is handled inside `docker-compose.yml`.

## How to Run Locally Without Docker

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
py -m uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## How to Run With Docker Compose

Make sure Docker Desktop is running.

From the project root folder, run:

```bash
docker compose up --build
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

To stop the containers:

```bash
Ctrl + C
```

To start again without rebuilding:

```bash
docker compose up
```

## API Endpoints

### Health

```http
GET /health
```

### Cloud Services

```http
GET /services
GET /services/{service_id}
POST /services
```

### Incidents

```http
GET /incidents
GET /incidents/{incident_id}
POST /incidents
PATCH /incidents/{incident_id}/resolve
```

### Full Incident View

```http
GET /incidents/full
```

### Reports

```http
GET /reports/severity-summary
GET /reports/status-summary
GET /reports/service-risk
```

### Incident Intelligence

```http
GET /incidents/{incident_id}/summary
```

## Example Service Request

```json
{
  "name": "notification-service",
  "category": "worker",
  "environment": "production",
  "status": "healthy",
  "owner_team": "platform"
}
```

## Example Incident Request

```json
{
  "service_id": 2,
  "title": "New payment error spike",
  "severity": "high",
  "status": "open",
  "latency_ms": 1200,
  "error_count": 150,
  "created_at": "2026-09-08 15:20",
  "resolved_at": null
}
```

## Example Service Risk Response

```json
{
  "service_id": 2,
  "service_name": "payment-service",
  "owner_team": "payments",
  "total_incidents": 3,
  "open_incidents": 2,
  "critical_incidents": 1,
  "total_errors": 580,
  "avg_latency": 1850.5
}
```

## Example Incident Summary Response

```json
{
  "incident_id": 1,
  "summary": "payment-service has a critical open incident with 430 errors and 2500ms latency.",
  "recommended_action": "Escalate to payments team immediately."
}
```

## What I Learned

This project includes:

- FastAPI routing
- Pydantic validation
- PostgreSQL connection handling
- SQL INSERT, SELECT, UPDATE
- JOIN and LEFT JOIN
- GROUP BY reports
- COUNT, SUM, AVG
- COALESCE for NULL handling
- HTTP error handling
- clean backend project structure
- Dockerfile creation
- Docker Compose with FastAPI and PostgreSQL
- rule-based incident intelligence logic

## Future Improvements

- Deploy to AWS EC2
- Add authentication
- Add real LLM-based incident summaries
- Add logging and monitoring
- Add automated tests
- Add CI/CD pipeline