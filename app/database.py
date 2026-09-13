import psycopg2

from app.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def get_connection():
    connection  = psycopg2.connect(
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cloud_services (
        service_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL CHECK (category IN ('backend', 'database', 'ai', 'worker', 'gateway', 'frontend')),
        environment TEXT NOT NULL CHECK (environment IN ('development', 'staging', 'production')),
        status TEXT NOT NULL CHECK (status IN ('healthy', 'degraded', 'down')),
        owner_team TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
        incident_id SERIAL PRIMARY KEY,
        service_id INTEGER NOT NULL REFERENCES cloud_services(service_id),
        title TEXT NOT NULL,
        severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
        status TEXT NOT NULL CHECK (status IN ('open', 'investigating', 'resolved')),
        latency_ms INTEGER NOT NULL CHECK (latency_ms >= 0),
        error_count INTEGER NOT NULL CHECK (error_count >= 0),
        created_at TEXT NOT NULL,
        resolved_at TEXT
        )
    """)
    connection.commit()
    connection.close()

def seed_cloud_services():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM cloud_services")
    count = cursor.fetchone()[0]
    if count > 0:
        connection.close()
        return
    services = [
        ("api-gateway", "gateway", "production", "healthy", "platform"),
        ("payment-service", "backend", "production", "degraded", "payments"),
        ("auth-service", "backend", "production", "healthy", "security"),
        ("main-database", "database", "production", "degraded", "database"),
        ("ai-service", "ai", "staging", "healthy", "ai-team")
    ]


    cursor.executemany("""
        INSERT INTO cloud_services (
        name,
        category,
        environment,
        status,
        owner_team
        )
        VALUES(%s, %s, %s, %s, %s)
    """, services)
    connection.commit()
    connection.close()

def seed_incidents():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]

    if count > 0:
        connection.close()
        return

    incidents = [
            (2, "High payment latency", "critical", "open", 2500, 430, "2026-09-04 10:00", None),
            (4, "Database timeout errors", "high", "investigating", 1800, 210, "2026-09-04 10:20", None),
            (1, "Gateway error spike", "medium", "open", 700, 80, "2026-09-04 10:40", None)
    ]
    cursor.executemany("""
        INSERT INTO incidents (
        service_id,
        title,
        severity,
        status,
        latency_ms,
        error_count,
        created_at,
        resolved_at
        )
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    """, incidents)
    connection.commit()
    connection.close()
    