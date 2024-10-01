from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate
from typing import Literal


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[Optional[str]]
    phone: Mapped[str]
    kpi: Mapped[float]
    role: Mapped[str]


class UserModelOut(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    phone: str
    kpi: float
    role: str


class UserModelIn(BaseModel):
    phone: str
    name: Optional[str]
    role: Literal["prorab", "worker"]


user_api = Blueprint("users", "users")


@user_api.route("/", methods=["POST"])
@validate()
def create_user(body: UserModelIn):
    new_user = User(name=body.name, phone=body.phone, kpi=0.0, role=body.role)
    search = session.execute(select(User).filter_by(phone=new_user.phone)).first()
    if search is None:
        session.add(new_user)
        session.commit()
        return (
            UserModelOut(
                name=new_user.name,
                phone=new_user.phone,
                id=new_user.id,
                kpi=new_user.kpi,
                role=new_user.role,
            ).model_dump(),
            201,
        )
    else:
        return ({"error": "user exists"}, 409)


@user_api.route("/")
@validate()
def list_users():
    q = select(User)
    users = session.scalars(q).all()
    return [
        UserModelOut(
            name=x.name, phone=x.phone, id=x.id, kpi=x.kpi, role=x.role
        ).model_dump()
        for x in users
    ]


@user_api.route("/<id>")
@validate()
def get_user(id: uuid.UUID):
    search = session.execute(select(User).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return UserModelOut(
            name=search.name,
            id=search.id,
            phone=search.phone,
            kpi=search.kpi,
            role=search.role,
        )
    else:
        return ({"error": "user not found"}, 404)


@user_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_user(id: uuid.UUID):
    search = session.execute(select(User).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "user not found"}, 404)


@user_api.route("/<id>/tasks", methods=["GET"])
@validate()
def get_tasks_from_user(id: uuid.UUID):
    from user_tasks import UserTask
    from tasks import Task, ModuleTaskOut

    search = session.execute(select(User).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "user not found"}, 404)
    tasks = session.scalars(select(Task).join(UserTask).filter_by(user_id=id)).all()
    return [
        ModuleTaskOut(
            description=x.description,
            id=x.id,
            deadline=x.deadline,
            work_scope=x.work_scope,
            object_id=x.object_id,
            done_scope=x.done_scope,
            plan_scope_hours=x.plan_scope_hours,
            user_count=x.user_count,
            plan_per_hour=x.plan_per_hour,
            shift=x.shift,
            plan_in_days=x.plan_in_days,
            start_date=x.start_date,
            user_count_by_plan=x.user_count_by_plan,
        ).model_dump()
        for x in tasks
    ]
