from app.database import get_connection
from datetime import datetime

def get_all_services():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        service_id,
        name,
        category,
        environment,
        status,
        owner_team
    FROM cloud_services""")

    rows = cursor.fetchall()

    services = []
    for row in rows:
        service = {
            "service_id": row[0],
            "name": row[1],
            "category": row[2],
            "environment": row[3],
            "status": row[4],
            "owner_team": row[5]
        }
        services.append(service)
    connection.close()
    return services

def get_service_by_id(service_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        service_id,
        name,
        category,
        environment,
        status,
        owner_team
    FROM cloud_services
    WHERE service_id = %s
""", (service_id,))

    row = cursor.fetchone()
    if row is None:
        connection.close()
        return None
    
    service = {
    "service_id": row[0],
    "name": row[1],
    "category": row[2],
    "environment": row[3],
    "status": row[4],
    "owner_team": row[5]
    }
    connection.close()
    return service

def create_service(service):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO cloud_services (
            name,
            category,
            environment,
            status,
            owner_team
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING service_id
    """, (
        service.name,
        service.category,
        service.environment,
        service.status,
        service.owner_team
    ))

    new_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return get_service_by_id(new_id)

def get_all_incidents():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            incident_id,
            service_id,
            title,
            severity,
            status,
            latency_ms,
            error_count,
            created_at,
            resolved_at
        FROM incidents
    """)

    rows = cursor.fetchall()

    incidents = []

    for row in rows:
        incident = {
            "incident_id": row[0],
            "service_id": row[1],
            "title": row[2],
            "severity": row[3],
            "status": row[4],
            "latency_ms": row[5],
            "error_count": row[6],
            "created_at": row[7],
            "resolved_at": row[8]
        }

        incidents.append(incident)

    connection.close()
    return incidents


def get_incident_by_id(incident_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            incident_id,
            service_id,
            title,
            severity,
            status,
            latency_ms,
            error_count,
            created_at,
            resolved_at
        FROM incidents
        WHERE incident_id = %s
    """, (incident_id,))

    row = cursor.fetchone()

    if row is None:
        connection.close()
        return None

    incident = {
        "incident_id": row[0],
        "service_id": row[1],
        "title": row[2],
        "severity": row[3],
        "status": row[4],
        "latency_ms": row[5],
        "error_count": row[6],
        "created_at": row[7],
        "resolved_at": row[8]
    }

    connection.close()
    return incident

def create_incident(incident):
    service = get_service_by_id(incident.service_id)
    if service is None:
        return "service_not_found"

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING incident_id
    """, (
        incident.service_id,
        incident.title,
        incident.severity,
        incident.status,
        incident.latency_ms,
        incident.error_count,
        incident.created_at,
        incident.resolved_at
    ))
    new_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return get_incident_by_id(new_id)

def resolve_incident(incident_id):
    incident = get_incident_by_id(incident_id)

    if incident is None:
        return "incident_not_found"

    if incident["status"] == "resolved":
        return "incident_already_resolved"

    connection = get_connection()
    cursor = connection.cursor()

    resolved_at = datetime.now().isoformat()

    cursor.execute("""
        UPDATE incidents
        SET status = %s,
            resolved_at = %s
        WHERE incident_id = %s
    """, ("resolved", resolved_at, incident_id))

    connection.commit()
    connection.close()

    return get_incident_by_id(incident_id)

def get_full_incidents():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(""" 
        SELECT
        incidents.incident_id,
        cloud_services.name,
        cloud_services.owner_team,
        cloud_services.environment,
        incidents.title,
        incidents.severity,
        incidents.status,
        incidents.latency_ms,
        incidents.error_count,
        incidents.created_at,
        incidents.resolved_at
        FROM incidents
        JOIN cloud_services
        ON incidents.service_id = cloud_services.service_id
    """)
    rows = cursor.fetchall()
    full = []
    for row in rows:
        incident = {
        "incident_id": row[0],
        "service_name": row[1],
        "owner_team": row[2],
        "environment": row[3],
        "title": row[4],
        "severity": row[5],
        "status": row[6],
        "latency_ms": row[7],
        "error_count": row[8],
        "created_at": row[9],
        "resolved_at": row[10]           
        }
        full.append(incident)

    connection.close()

    return full

def get_severity_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
        severity,
        COUNT(*)
        FROM incidents
        GROUP BY severity
    """)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        summary = {
            "severity": row[0],
            "count": row[1]
        }
        result.append(summary)
    connection.close()
    return result

def get_status_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
    status,
    COUNT(*)
    FROM incidents
    GROUP BY status
    """)
    rows = cursor.fetchall()
    result = []

    for row in rows:
        summary = {
            "status": row[0],
            "count": row[1]
        }
        result.append(summary)
    connection.close()
    return result


def get_service_risk_report():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        cloud_services.service_id,
        cloud_services.name,
        cloud_services.owner_team,
        COUNT(incidents.incident_id),
        COUNT(CASE WHEN incidents.status = 'open' THEN 1 END),
        COUNT(CASE WHEN incidents.severity = 'critical' THEN 1 END),
        COALESCE(SUM(incidents.error_count), 0),
        COALESCE(AVG(incidents.latency_ms), 0)
    FROM cloud_services
    LEFT JOIN incidents
    ON cloud_services.service_id = incidents.service_id
    GROUP BY
        cloud_services.service_id,
        cloud_services.name,
        cloud_services.owner_team    
    """)
    rows = cursor.fetchall()

    result = []

    for row in rows:
        service_risk = {
            "service_id": row[0],
            "service_name": row[1],
            "owner_team": row[2],
            "total_incidents": row[3],
            "open_incidents": row[4],
            "critical_incidents": row[5],
            "total_errors": row[6],
            "avg_latency": row[7]            
        }
        result.append(service_risk)

    connection.close()
    return result

def get_incident_summary(incident_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
    incidents.incident_id,
    cloud_services.name,
    cloud_services.owner_team,
    incidents.title,
    incidents.severity,
    incidents.status,
    incidents.latency_ms,
    incidents.error_count
    FROM incidents
    JOIN cloud_services
    ON incidents.service_id = cloud_services.service_id
    WHERE incidents.incident_id = %s
    """, (incident_id,))
    row = cursor.fetchone()
    if row is None:
        connection.close()
        return "incident_not_found"

    incident_id_from_db = row[0]
    service_name = row[1]
    owner_team = row[2]
    title = row[3]
    severity = row[4]
    status = row[5]
    latency_ms = row[6]
    error_count = row[7]

    summary = f"{service_name} has a {severity} {status} incident with {error_count} errors and {latency_ms}ms latency."
    if severity == "critical":
        recommended_action = f"Escalate to {owner_team} team immediately."
    elif severity == "high":
        recommended_action = f"Investigate with priority by {owner_team} team."
    elif severity == "medium":
        recommended_action = f"Monitor and investigate by {owner_team} team."
    else:
        recommended_action = "Monitor."

    connection.close()

    return {
        "incident_id": incident_id_from_db,
        "summary": summary,
        "recommended_action": recommended_action
    }