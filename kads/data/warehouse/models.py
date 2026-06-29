from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from kads.data.warehouse.db import Base

class DimCampaignState(Base):
    __tablename__ = "dim_campaign_state"

    campaign_id = Column(String, primary_key=True)
    campaign_name = Column(String, nullable=False)
    platform = Column(String, nullable=False)  # google, meta
    status = Column(String, nullable=False)    # active, paused, etc.
    budget = Column(Float, nullable=False)
    bid_strategy = Column(String, nullable=False)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

class FactAdPerformanceHourly(Base):
    __tablename__ = "fact_ad_performance_hourly"

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(String, ForeignKey("dim_campaign_state.campaign_id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    spend = Column(Float, default=0.0)
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)

class FactConversionEvent(Base):
    __tablename__ = "fact_conversion_event"

    event_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    platform = Column(String, nullable=False)  # google, meta, hms, etc.
    event_name = Column(String, nullable=False) # purchase, lead, begin_checkout, etc.
    value = Column(Float, default=0.0)
    currency = Column(String, default="TRY")
    click_id = Column(String, nullable=True)   # gclid, fbclid, etc.
    transaction_id = Column(String, nullable=True)
    crm_user_id = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)  # matched with HMS
    deduplicated = Column(Boolean, default=False)

class FactActionJournal(Base):
    __tablename__ = "fact_action_journal"

    action_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    platform = Column(String, nullable=False)
    entity_type = Column(String, nullable=False) # campaign, adset, etc.
    entity_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False) # pause, budget_change, etc.
    current_state = Column(JSON, nullable=False)
    proposed_state = Column(JSON, nullable=False)
    expected_impact = Column(String, nullable=True)
    risk_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    requires_approval = Column(Boolean, default=True)
    approval_reason = Column(JSON, nullable=True) # list of reasons
    rollback_plan = Column(JSON, nullable=True)
    status = Column(String, default="pending") # pending, approved, executed, etc.
    executed_at = Column(DateTime, nullable=True)

class FactTrackingHealth(Base):
    __tablename__ = "fact_tracking_health"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now())
    component = Column(String, nullable=False) # GA4, GTM, Pixel, CAPI, OCT
    status = Column(String, nullable=False)    # healthy, stale, error
    score = Column(Float, nullable=False)      # 0.0 to 100.0
    details = Column(JSON, nullable=True)
