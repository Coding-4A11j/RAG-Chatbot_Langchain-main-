import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    owner = "owner"
    admin = "admin"
    manager = "manager"
    rep = "rep"


class RecordStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    archived = "archived"


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), unique=True)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False, default=UserRole.rep)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class Company(Base, TimestampMixin):
    __tablename__ = "companies"
    __table_args__ = (Index("ix_companies_org_name", "organization_id", "name"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(512))
    industry: Mapped[Optional[str]] = mapped_column(String(128))
    employee_size: Mapped[Optional[int]] = mapped_column(Integer)
    country: Mapped[Optional[str]] = mapped_column(String(128))


class Lead(Base, TimestampMixin):
    __tablename__ = "leads"
    __table_args__ = (Index("ix_leads_org_status_owner", "organization_id", "status", "owner_user_id"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id: Mapped[Optional[str]] = mapped_column(ForeignKey("companies.id", ondelete="SET NULL"), index=True)
    owner_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(128))
    last_name: Mapped[Optional[str]] = mapped_column(String(128))
    email: Mapped[Optional[str]] = mapped_column(String(320), index=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(255))
    source: Mapped[Optional[str]] = mapped_column(String(100))
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[RecordStatus] = mapped_column(Enum(RecordStatus, name="lead_status"), default=RecordStatus.active, nullable=False)


class Deal(Base, TimestampMixin):
    __tablename__ = "deals"
    __table_args__ = (Index("ix_deals_org_stage_owner", "organization_id", "pipeline_stage", "owner_user_id"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id: Mapped[Optional[str]] = mapped_column(ForeignKey("companies.id", ondelete="SET NULL"), index=True)
    lead_id: Mapped[Optional[str]] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), index=True)
    owner_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    pipeline_stage: Mapped[str] = mapped_column(String(80), nullable=False, default="new")
    value_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[RecordStatus] = mapped_column(Enum(RecordStatus, name="deal_status"), default=RecordStatus.active, nullable=False)
    close_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class Meeting(Base, TimestampMixin):
    __tablename__ = "meetings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    owner_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    lead_id: Mapped[Optional[str]] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), index=True)
    deal_id: Mapped[Optional[str]] = mapped_column(ForeignKey("deals.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[RecordStatus] = mapped_column(Enum(RecordStatus, name="meeting_status"), default=RecordStatus.active, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"
    __table_args__ = (Index("ix_tasks_org_assignee_status", "organization_id", "assigned_to_user_id", "status"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_to_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    related_lead_id: Mapped[Optional[str]] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), index=True)
    related_deal_id: Mapped[Optional[str]] = mapped_column(ForeignKey("deals.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="todo", nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    due_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    author_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    lead_id: Mapped[Optional[str]] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), index=True)
    deal_id: Mapped[Optional[str]] = mapped_column(ForeignKey("deals.id", ondelete="SET NULL"), index=True)
    company_id: Mapped[Optional[str]] = mapped_column(ForeignKey("companies.id", ondelete="SET NULL"), index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class Campaign(Base, TimestampMixin):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="email", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class Email(Base, TimestampMixin):
    __tablename__ = "emails"
    __table_args__ = (Index("ix_emails_org_status_sent", "organization_id", "status", "sent_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    lead_id: Mapped[Optional[str]] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), index=True)
    deal_id: Mapped[Optional[str]] = mapped_column(ForeignKey("deals.id", ondelete="SET NULL"), index=True)
    campaign_id: Mapped[Optional[str]] = mapped_column(ForeignKey("campaigns.id", ondelete="SET NULL"), index=True)
    subject: Mapped[Optional[str]] = mapped_column(String(512))
    body: Mapped[Optional[str]] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(String(50), default="cold", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    opened_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    replied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (Index("ix_activities_org_entity_time", "organization_id", "entity_type", "created_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    actor_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AILog(Base, TimestampMixin):
    __tablename__ = "ai_logs"
    __table_args__ = (Index("ix_ai_logs_org_agent_created", "organization_id", "agent_name", "created_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_name: Mapped[str] = mapped_column(String(120), nullable=False)
    operation: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="success")
    input_text: Mapped[Optional[str]] = mapped_column(Text)
    output_text: Mapped[Optional[str]] = mapped_column(Text)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_logs_org_action_created", "organization_id", "action", "created_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(120), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(36), index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64))
    user_agent: Mapped[Optional[str]] = mapped_column(String(512))
    details_json: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"
    __table_args__ = (Index("ix_subscriptions_org_status", "organization_id", "status"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    plan_name: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(60), nullable=False)
    current_period_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class BillingRecord(Base, TimestampMixin):
    __tablename__ = "billing_records"
    __table_args__ = (Index("ix_billing_records_org_issued", "organization_id", "issued_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    subscription_id: Mapped[Optional[str]] = mapped_column(ForeignKey("subscriptions.id", ondelete="SET NULL"), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    issued_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))


class Integration(Base, TimestampMixin):
    __tablename__ = "integrations"
    __table_args__ = (Index("ix_integrations_org_provider", "organization_id", "provider"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    external_account_id: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="connected")
    config_json: Mapped[Optional[dict]] = mapped_column(JSON)
