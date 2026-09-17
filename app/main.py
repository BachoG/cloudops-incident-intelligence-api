from fastapi import FastAPI, HTTPException, Depends
from app.database import init_db, seed_cloud_services, seed_incidents
from app.schemas import CloudServiceCreate, CloudServiceResponse, IncidentCreate, IncidentResponse, FullIncidentResponse, SeveritySummaryResponse, StatusSummaryResponse, ServiceRiskResponse, IncidentSummaryResponse
from app.services import get_all_services, get_service_by_id, create_service, get_all_incidents, create_incident, get_incident_by_id, resolve_incident, get_full_incidents, get_severity_summary, get_status_summary, get_service_risk_report, get_incident_summary
from app.auth import verify_api_key

app = FastAPI(title="CloudOps Incident Intelligence API")
init_db()
seed_cloud_services()
seed_incidents()


@app.get("/health")
def show_health():
    return {
    "status": "ok",
    "project": "cloudops-incident-intelligence-api-v2"
    }

@app.get("/services", response_model=list[CloudServiceResponse])
def read_all_services():
    return get_all_services()

@app.get("/services/{service_id}", response_model=CloudServiceResponse)
def show_service_by_id(service_id: int):
    service = get_service_by_id(service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="service_not_found")
    return service

@app.post("/services", response_model=CloudServiceResponse)
def create_new_cloud_service(service: CloudServiceCreate, _api_key: str = Depends(verify_api_key)):
    return create_service(service)

@app.get("/incidents", response_model=list[IncidentResponse])
def read_all_incidents():
    return get_all_incidents()

@app.patch("/incidents/{incident_id}/resolve", response_model=IncidentResponse)
def resolve_existing_incident(incident_id: int):
    result = resolve_incident(incident_id)

    if result == "incident_not_found":
        raise HTTPException(status_code=404, detail="incident_not_found")

    if result == "incident_already_resolved":
        raise HTTPException(status_code=400, detail="incident_already_resolved")

    return result    

@app.get("/incidents/full", response_model=list[FullIncidentResponse])
def show_full_incidents():
    return get_full_incidents()

@app.get("/incidents/{incident_id}", response_model=IncidentResponse)
def show_incident_by_id(incident_id: int):
    incident = get_incident_by_id(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="incident_not_found")
    return incident

@app.post("/incidents", response_model=IncidentResponse)
def create_new_incident(incident: IncidentCreate):
    result = create_incident(incident)
    if result == "service_not_found":
        raise HTTPException(status_code=404, detail="service_not_found")
    return result

@app.get("/reports/severity-summary", response_model=list[SeveritySummaryResponse])
def show_severity_summary():
    return get_severity_summary()
@app.get("/reports/status-summary", response_model=list[StatusSummaryResponse])
def show_status_summary():
    return get_status_summary()

@app.get("/reports/service-risk", response_model=list[ServiceRiskResponse])
def show_service_risk_report():
    return get_service_risk_report()

@app.get("/incidents/{incident_id}/summary", response_model=IncidentSummaryResponse)
def show_incident_summary(incident_id: int):
    result = get_incident_summary(incident_id)

    if result == "incident_not_found":
        raise HTTPException(status_code=404, detail="incident_not_found")

    return result