from pydantic import BaseModel, Field
from typing import Literal

class CloudServiceCreate(BaseModel):
    name: str = Field(min_length=1)
    category: Literal["backend", "database", "ai", "worker", "gateway", "frontend"]
    environment: Literal["development", "staging", "production"]
    status: Literal["healthy", "degraded", "down"]
    owner_team: str = Field(min_length=1)

class CloudServiceResponse(BaseModel):
    service_id: int = Field(ge=1)
    name: str = Field(min_length=1)
    category: Literal["backend", "database", "ai", "worker", "gateway", "frontend"]
    environment: Literal["development", "staging", "production"]
    status: Literal["healthy", "degraded", "down"]
    owner_team: str = Field(min_length=1)

class IncidentCreate(BaseModel):
    service_id: int = Field(ge=1)
    title: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "investigating", "resolved"]
    latency_ms: int = Field(ge=0)
    error_count: int = Field(ge=0)
    created_at: str = Field(min_length=1)
    resolved_at: str | None = None

class IncidentResponse(BaseModel):
    incident_id: int = Field(ge=1)
    service_id: int = Field(ge=1)
    title: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "investigating", "resolved"]
    latency_ms: int = Field(ge=0)
    error_count: int = Field(ge=0)
    created_at: str = Field(min_length=1)
    resolved_at: str | None = None

class FullIncidentResponse(BaseModel):
    incident_id: int = Field(ge=1)
    service_name: str = Field(min_length=1)
    owner_team: str = Field(min_length=1)
    environment: Literal["development", "staging", "production"]
    title: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "investigating", "resolved"]
    latency_ms: int = Field(ge=0)
    error_count: int = Field(ge=0)
    created_at: str = Field(min_length=1)
    resolved_at: str | None = None

class SeveritySummaryResponse(BaseModel):
    severity: Literal["low", "medium", "high", "critical"]
    count: int = Field(ge = 0)

class StatusSummaryResponse(BaseModel):
    status: Literal["open", "investigating", "resolved"]
    count: int = Field(ge=0)

class ServiceRiskResponse(BaseModel):
    service_id: int = Field(ge=1)
    service_name: str = Field(min_length=1)
    owner_team: str = Field(min_length=1)
    total_incidents: int = Field(ge=0)
    open_incidents: int = Field(ge=0)
    critical_incidents: int = Field(ge=0)
    total_errors: int = Field(ge=0)
    avg_latency: float = Field(ge=0)

class IncidentSummaryResponse(BaseModel):
    incident_id: int = Field(ge=1)
    summary: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)