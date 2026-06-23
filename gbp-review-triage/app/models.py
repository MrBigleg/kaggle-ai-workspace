from pydantic import BaseModel, Field


class ReviewInput(BaseModel):
    review_id: str = Field(description="Unique identifier for the review")
    location_id: str = Field(description="Google Business Profile location identifier")
    rating: int = Field(description="Star rating from 1 to 5")
    author_name: str = Field(description="Name of the reviewer")
    comment: str = Field(description="Text comment left by the user")


class LocationProfile(BaseModel):
    location_id: str
    name: str
    brand_voice_tone: str
    specialty: str


class TriageResult(BaseModel):
    review_id: str
    status: str = Field(description="Triage status: 'replied' or 'flagged'")
    reply_text: str | None = Field(
        default=None, description="Generated response if status is 'replied'"
    )
    flag_reason: str | None = Field(
        default=None, description="Reason for flagging if status is 'flagged'"
    )
    redacted_categories: list[str] | None = Field(
        default=None, description="Categories of PII redacted from the review comment"
    )
