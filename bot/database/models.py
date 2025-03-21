from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from bot.database import Base

# statistics.py

class Screams(Base):
    __tablename__ = "screams"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    total: Mapped[int]
    streak: Mapped[int]
    streak_last = Mapped[int]
    best_streak: Mapped[int]
    daily: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    streak_keeper: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return (
            f"<Screams("
            f"user_id={self.user_id},"
            f"total={self.total},"
            f"streak={self.streak},"
            f"best_streak={self.best_streak},"
            f"daily={self.daily},"
            f"streak_keeper={self.streak_keeper}"
            ")>"
        )


class StatisticsConfig(Base):
    __tablename__ = "statistics_config"
    guild_id = mapped_column(BigInteger, primary_key=True)
    regexp_primary: Mapped[Optional[str]]
    regexp_secondary: Mapped[Optional[str]]
    channel_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    minor_threshold: Mapped[Optional[int]]
    major_threshold: Mapped[Optional[int]]
    minor_role_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    major_role_id: Mapped[Optional[int]] = mapped_column(BigInteger)


# reminder.py

class Reminder(Base):
    __tablename__ = "reminders"
    id: Mapped[int] = mapped_column(Identity(start=1, cycle=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    message: Mapped[str]
    send_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    requested_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    repeat: Mapped[bool]

    def __repr__(self):
        return (
            f"<Reminder("
            f"id={self.id},"
            f"user_id={self.user_id},"
            f"channel_id={self.channel_id},"
            f"message={self.message},"
            f"send_time={self.send_time},"
            f"requested_time={self.requested_time},"
            f"repeat={self.repeat}"
            ")>"
        )

    def __iter__(self):
        return iter(
            (self.id, self.user_id, self.channel_id, self.message, self.send_time, self.requested_time, self.repeat)
        )


# courses.py

class Course(Base):
    __tablename__ = "courses"
    guild_id = mapped_column(BigInteger, primary_key=True)
    course_code: Mapped[str] = mapped_column(primary_key=True)
    
    def __repr__(self):
        return (
            f"<Course("
            f"guild_id={self.guild_id},"
            f"course_code={self.course_code}"
            ")>"
        )

class CourseChannel(Base):
    __tablename__ = "course_channels"
    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    course_code: Mapped[str] = mapped_column(primary_key=True)
    do_not_reset: Mapped[bool]

    def __repr__(self):
        return (
            f"<CourseChannel("
            f"channel_id={self.channel_id},"
            f"guild_id={self.guild_id},"
            f"course_code={self.course_code},"
            f"do_not_reset={self.do_not_reset}"
            ")>"
        )


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

    __table_args__ = (
        ForeignKeyConstraint(
            ["channel_id", "guild_id", "course_code"],
            ["course_channels.channel_id", "course_channels.guild_id", "course_channels.course_code"],
        ),
        {},
    )

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    course_code: Mapped[str] = mapped_column(primary_key=True)

    channel = relationship(
        "CourseChannel",
        foreign_keys=[channel_id, guild_id, course_code],
        backref=backref("course_enrollments", cascade="all, delete-orphan"),
    )

    def __repr__(self):
        return (
            f"<CourseEnrollment("
            f"user_id={self.user_id},"
            f"channel_id={self.channel_id},"
            f"guild_id={self.guild_id}"
            f"course_code={self.course_code}"
            ")>"
        )

class CourseConfig(Base):
    __tablename__ = "course_config"
    guild_id = mapped_column(BigInteger, primary_key=True)
    auto_delete: Mapped[Optional[bool]]
    auto_delete_ignore_admins: Mapped[Optional[bool]]

    def __repr__(self):
        return (
            f"<CourseConfig("
            f"guild_id={self.guild_id},"
            f"auto_delete={self.auto_delete},"
            f"auto_delete_ignore_admins={self.auto_delete_ignore_admins}"
            ")>"
        )
