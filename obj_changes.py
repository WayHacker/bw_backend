from flask import request, Blueprint, jsonify
from typing import List
from typing import Optional
from sqlalchemy import String, text, select, and_
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from db import Base, session
from pydantic import BaseModel
from flask_pydantic import validate
import datetime


class Change(Base):
    __tablename__ = "changes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    object_id: Mapped[uuid.UUID]
    name: Mapped[Optional[str]]
    date: Mapped[datetime.datetime]
    days: Mapped[int]
    reasons: Mapped[str]
    who_change: Mapped[uuid.UUID]
    task_id: Mapped[Optional[uuid.UUID]]


class ChangeModelIn(BaseModel):
    name: str
    who_change: uuid.UUID
    days: Optional[int] = 0
    reasons: str
    object_id: uuid.UUID
    task_id: Optional[uuid.UUID] = None


class ChangeModelOut(BaseModel):
    name: str
    id: uuid.UUID
    date: datetime.datetime
    who_change: uuid.UUID
    days: int
    reasons: str
    task_id: Optional[uuid.UUID] = None


changes_api = Blueprint("changes", "changes")
"""TODO task id if it change -> change task -> auto update days of task deadline"""


@changes_api.route("/", methods=["POST"])
@validate()
def create_Change(body: ChangeModelIn):
    new_change = Change(
        name=body.name,
        object_id=body.object_id,
        date=datetime.datetime.now(),
        days=body.days,
        reasons=body.reasons,
        who_change=body.who_change,
    )
    session.add(new_change)
    session.commit()
    return (
        ChangeModelOut(
            name=new_change.name,
            id=new_change.id,
            object_id=new_change.object_id,
            who_change=new_change.who_change,
            reasons=new_change.reasons,
            date=new_change.date,
            days=new_change.days,
        ),
        201,
    )


@changes_api.route("/", methods=["GET"])
@validate()
def list_Changes():
    q = select(Change)
    changes = session.scalars(q).all()
    return [
        ChangeModelOut(
            name=x.name,
            id=x.id,
            object_id=x.object_id,
            who_change=x.who_change,
            reasons=x.reasons,
            date=x.date,
            days=x.days,
        ).model_dump()
        for x in changes
    ]


@changes_api.route("/<id>", methods=["GET"])
@validate()
def get_change(id: uuid.UUID):
    search = session.execute(select(Change).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (
            ChangeModelOut(
                name=search.name,
                id=search.id,
                object_id=search.object_id,
                who_change=search.who_change,
                reasons=search.reasons,
                date=search.date,
                days=search.days,
            ).model_dump(),
            200,
        )
    else:
        return ({"error": "Change not found"}, 404)


@changes_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_change(id: uuid.UUID):
    search = session.execute(select(Change).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "Change not found"}, 404)
