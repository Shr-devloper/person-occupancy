from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import CameraStatus, OccupancyState, UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.viewer


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CameraBase(BaseModel):
    camera_name: str = Field(min_length=2, max_length=120)
    location: str = Field(min_length=2, max_length=255)
    ip_address: str | None = None
    stream_url: str | None = None
    status: CameraStatus = CameraStatus.offline


class CameraCreate(CameraBase):
    pass


class CameraUpdate(BaseModel):
    camera_name: str | None = Field(default=None, min_length=2, max_length=120)
    location: str | None = Field(default=None, min_length=2, max_length=255)
    ip_address: str | None = None
    stream_url: str | None = None
    status: CameraStatus | None = None


class CameraRead(CameraBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SeatCreate(BaseModel):
    seat_name: str = Field(min_length=2, max_length=120)
    camera_id: int
    region_x1: int = Field(ge=0)
    region_y1: int = Field(ge=0)
    region_x2: int = Field(ge=0)
    region_y2: int = Field(ge=0)


class SeatRead(SeatCreate):
    id: int
    current_state: OccupancyState
    last_state_change: datetime | None

    model_config = ConfigDict(from_attributes=True)


class OccupancyEventCreate(BaseModel):
    seat_id: int
    state: OccupancyState
    event_time: datetime
    camera_id: int | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)


class OccupancyLogRead(BaseModel):
    id: int
    seat_id: int
    start_time: datetime
    end_time: datetime | None
    duration: int

    model_config = ConfigDict(from_attributes=True)


class AnalyticsPoint(BaseModel):
    label: str
    occupied_seconds: int
    occupancy_percentage: float


class SeatUsage(BaseModel):
    seat_id: int
    seat_name: str
    occupied_seconds: int


class DashboardAnalytics(BaseModel):
    total_seats: int
    occupied_seats: int
    available_seats: int
    occupancy_percentage: float
    camera_status: dict[str, int]
    daily: list[AnalyticsPoint]
    weekly: list[AnalyticsPoint]
    monthly: list[AnalyticsPoint]
    peak_usage_hours: list[AnalyticsPoint]
    most_used_seats: list[SeatUsage]
    least_used_seats: list[SeatUsage]


class NotificationRead(BaseModel):
    id: int
    title: str
    message: str
    severity: str
    seat_id: int | None
    camera_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceTokenCreate(BaseModel):
    token: str = Field(min_length=20, max_length=512)
    platform: str = Field(pattern="^(android|ios|web)$")


class DateRange(BaseModel):
    start: date
    end: date
