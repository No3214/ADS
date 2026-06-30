from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class RiskSchema(BaseModel):
    risk_score: float = Field(
        ..., ge=0.0, le=1.0, description="Calculated risk score between 0.0 and 1.0"
    )
    risk_level: Literal["low", "medium", "high", "critical"] = Field(
        ..., description="Risk tier based on score"
    )
    reasons: List[str] = Field(
        default_factory=list,
        description="List of reasons contributing to this risk score",
    )
    required_action: Literal["none", "human_approval", "block"] = Field(
        ..., description="Required path forward based on risk"
    )


class ActionSchema(BaseModel):
    action_id: str = Field(..., description="Unique action identifier")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    platform: Literal["google", "meta", "seo", "general"] = Field(
        ..., description="Target platform"
    )
    entity_type: Literal[
        "campaign", "adset", "adgroup", "creative", "keyword", "budget"
    ] = Field(..., description="Type of target advertising entity")
    entity_id: str = Field(..., description="ID of the entity this action operates on")
    action_type: Literal[
        "pause",
        "budget_decrease",
        "budget_increase",
        "creative_test",
        "keyword_negative",
        "bid_adjustment",
    ] = Field(..., description="Action category")
    current_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="Attributes of the entity before action execution",
    )
    proposed_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="Attributes of the entity after action execution",
    )
    expected_impact: str = Field(..., description="Brief summary of expected results")
    risk_score: float = Field(
        ..., ge=0.0, le=1.0, description="Risk score associated with this action"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Agent confidence score")
    requires_approval: bool = Field(
        default=True, description="Whether this action requires human review"
    )
    approval_reason: List[str] = Field(
        default_factory=list, description="Reason(s) why this action requires approval"
    )
    rollback_plan: Dict[str, Any] = Field(
        default_factory=dict, description="Reversal instructions/parameters"
    )
    expires_at: Optional[datetime] = Field(
        None, description="Expiry timestamp of the approval request"
    )
    status: Literal[
        "pending", "approved", "rejected", "executed", "failed", "rolled_back"
    ] = Field("pending", description="Lifecycle state of the action")


class CampaignStateSchema(BaseModel):
    campaign_id: str = Field(..., description="Platform campaign ID")
    campaign_name: str = Field(..., description="Campaign name")
    platform: Literal["google", "meta"] = Field(..., description="Advertising network")
    status: Literal["active", "paused", "removed", "unknown"] = Field(
        ..., description="Current status"
    )
    budget: float = Field(..., ge=0.0, description="Daily or lifetime budget value")
    bid_strategy: str = Field(..., description="Bid strategy type")
    metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Performance metrics dictionary (spend, conversions, impressions, etc.)",
    )
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Last sync timestamp"
    )
