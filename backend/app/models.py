import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    viewer = "viewer"


class CameraStatus(str, enum.Enum):
    online = "online"
    offline = "offline"
    maintenance = "maintenance"


class OccupancyState(str, enum.Enum):
    occupied = "occupied"
    empty = "empty"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.viewer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    device_tokens: Mapped[list["DeviceToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True)
    camera_name: Mapped[str] = mapped_column(String(120), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stream_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[CameraStatus] = mapped_column(Enum(CameraStatus), default=CameraStatus.offline, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    seats: Mapped[list["Seat"]] = relationship(back_populates="camera", cascade="all, delete-orphan")


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True)
    seat_name: Mapped[str] = mapped_column(String(120), nullable=False)
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False)
    region_x1: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    region_y1: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    region_x2: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    region_y2: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_state: Mapped[OccupancyState] = mapped_column(Enum(OccupancyState), default=OccupancyState.empty, nullable=False)
    last_state_change: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    camera: Mapped[Camera] = relationship(back_populates="seats")
    logs: Mapped[list["OccupancyLog"]] = relationship(back_populates="seat", cascade="all, delete-orphan")


class OccupancyLog(Base):
    __tablename__ = "occupancy_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id", ondelete="CASCADE"), index=True, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    seat: Mapped[Seat] = relationship(back_populates="logs")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="info", nullable=False)
    seat_id: Mapped[int | None] = mapped_column(ForeignKey("seats.id", ondelete="SET NULL"), nullable=True)
    camera_id: Mapped[int | None] = mapped_column(ForeignKey("cameras.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped[User] = relationship(back_populates="device_tokens")
