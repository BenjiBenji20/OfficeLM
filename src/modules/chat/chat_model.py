from datetime import datetime, timezone
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List, Optional
import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, TimestampMixin, uuid_pk

if TYPE_CHECKING:
    from modules.authentication.auth_model import User


class ChatMemberRole(str, PyEnum):
    """Chat room member's role."""
    ADMIN = "ADMIN"
    USER = "USER"


class ChatMessageRole(str, PyEnum):
    """Role of the message sender in a chat room."""
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"


class FileJobStatus(str, PyEnum):
    """Lifecycle status of a generated document job."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class FileType(str, PyEnum):
    """Supported export file formats for document generation."""
    MD = "MD"
    DOCX = "DOCX"
    XLSX = "XLSX"
    PDF = "PDF"


class ChatRoom(Base, TimestampMixin):
    """Holds chat room details and metadata."""

    __tablename__ = "chat_rooms"
    __table_args__ = {"schema": "chat"}

    id: Mapped[uuid_pk]
    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        default="OfficeLM Default Group Chat",
        unique=False,
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_private: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    creator: Mapped["User"] = relationship(
        "User",
        back_populates="created_rooms",
    )
    members: Mapped[List["ChatRoomMember"]] = relationship(
        "ChatRoomMember",
        back_populates="room",
        cascade="all, delete-orphan",
    )
    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="room",
        cascade="all, delete-orphan",
    )


class ChatRoomMember(Base, TimestampMixin):
    """Junction table mapping users to chat rooms with room-level roles."""

    __tablename__ = "chat_room_members"
    __table_args__ = {"schema": "chat"}

    chat_room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat.chat_rooms.id", ondelete="CASCADE"),
        primary_key=True,
    )
    member_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role: Mapped[ChatMemberRole] = mapped_column(
        Enum(ChatMemberRole, native_enum=True),
        default=ChatMemberRole.USER,
        index=True,
        nullable=False,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    room: Mapped["ChatRoom"] = relationship(
        "ChatRoom",
        back_populates="members",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="room_memberships",
    )


class ChatMessage(Base, TimestampMixin):
    """Holds user, AI assistant, and system messages inside a chat room."""

    __tablename__ = "chat_messages"
    __table_args__ = {"schema": "chat"}

    id: Mapped[uuid_pk]
    chat_room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat.chat_rooms.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    role: Mapped[ChatMessageRole] = mapped_column(
        Enum(ChatMessageRole, native_enum=True),
        default=ChatMessageRole.USER,
        index=True,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    room: Mapped["ChatRoom"] = relationship(
        "ChatRoom",
        back_populates="messages",
    )
    sender: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="messages",
    )
    file_jobs: Mapped[List["FileJob"]] = relationship(
        "FileJob",
        back_populates="message",
        cascade="all, delete-orphan",
    )


class FileJob(Base, TimestampMixin):
    """Tracks asynchronous document generation tasks resulting from chat intents."""

    __tablename__ = "file_jobs"
    __table_args__ = {"schema": "chat"}

    id: Mapped[uuid_pk]
    message_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat.chat_messages.id", ondelete="CASCADE"),
        index=True,
        nullable=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    file_type: Mapped[FileType] = mapped_column(
        Enum(FileType, native_enum=True),
        index=True,
        nullable=False,
    )
    status: Mapped[FileJobStatus] = mapped_column(
        Enum(FileJobStatus, native_enum=True),
        default=FileJobStatus.PENDING,
        index=True,
        nullable=False,
    )
    output_path: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    message: Mapped[Optional["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="file_jobs",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="file_jobs",
    )
