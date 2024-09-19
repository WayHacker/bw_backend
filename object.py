from flask import request, Blueprint, jsonify
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate


class ObjectModelIn(BaseModel):
    name: str


class ObjectModelOut(BaseModel):
    name: str
    id: uuid.UUID


class Object(Base):
    __tablename__ = "object"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[Optional[str]]


def object_to_dict(obj):
    return {"id": obj.id, "name": obj.name}


object_api = Blueprint("objects", "objects")


@object_api.route("/", methods=["POST"])
@validate()
def create_object(body: ObjectModelIn):
    data = body.name
    new_object = Object(name=data)
    search = session.execute(select(Object).filter_by(name=new_object.name)).first()
    if search is None:
        session.add(new_object)
        session.commit()
        # return (object_to_dict(new_object), 201)
        return ObjectModelOut(name=new_object.name, id=new_object.id), 201
    else:
        return ({"error": "object exists"}, 409)


@object_api.route("/", methods=["GET"])
@validate()
def list_objects():
    q = select(Object)
    objects = session.scalars(q).all()
    # new_dict = [object_to_dict(x) for x in objects]
    return [ObjectModelOut(name=x.name, id=x.id).model_dump() for x in objects]


@object_api.route("/<id>", methods=["GET"])
@validate()
def get_object(id: uuid.UUID):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return ObjectModelOut(name=search.name, id=id).model_dump(), 200
    else:
        return ({"error": "object not found"}, 404)


@object_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_object(id: uuid.UUID):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "object not found"}, 404)


@object_api.route("/<id>/users", methods=["GET"])
@validate()
def get_users_from_object(id: uuid.UUID):
    from assignment import Assignment
    from user import User, UserModelOut

    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "object not found"}, 404)
    users = session.scalars(select(User).join(Assignment).filter_by(object_id=id)).all()
    return [
        UserModelOut(name=x.name, phone=x.phone, id=x.id).model_dump() for x in users
    ]


@object_api.route("/<id>/tasks", methods=["GET"])
@validate()
def get_all_tasks_from_object(id: uuid.UUID):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "object not found"}, 404)
    from tasks import Task, ModuleTaskOut

    tasks = session.scalars(select(Task).filter_by(object_id=id)).all()

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


@object_api.route("/<id>/done_tasks", methods=["GET"])
@validate()
def get_done_tasks_from_object(id: uuid.UUID):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "object not found"}, 404)
    from tasks import Task, ModuleTaskOut

    tasks = session.scalars(
        select(Task).where(
            and_(id == Task.object_id, Task.done_scope == Task.work_scope)
        )
    ).all()
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


@object_api.route("/<id>/undone_tasks", methods=["GET"])
@validate()
def get_undone_tasks_from_object(id: uuid.UUID):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "object not found"}, 404)
    from tasks import Task, ModuleTaskOut

    tasks = session.scalars(
        select(Task).where(
            and_(id == Task.object_id, Task.done_scope != Task.work_scope)
        )
    ).all()
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


def calculate_fact(id):
    from tasks import Task, ModuleTaskOut

    stmt = session.scalars(select(Task).filter_by(object_id=id)).all()

    all_tasks = [
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
            plan_in_days=x.plan_in_days,
            shift=x.shift,
            user_count_by_plan=x.user_count_by_plan,
            start_date=x.start_date,
        ).model_dump()
        for x in stmt
    ]
    all_v = 0
    done_v = 0
    for index in range(len(all_tasks)):
        for key in all_tasks[index]:
            if key == "plan_scope_hours":
                all_v += all_tasks[index][key]
            if key == "done_scope":
                done_v += all_tasks[index][key]

    print(all_v, done_v)
    return {"fact": (done_v / all_v) * 100}


def calculate_plan_and_predict(id):
    from tasks import Task, ModuleTaskOut
    from datetime import datetime, timedelta

    stmt = session.scalars(select(Task).filter_by(object_id=id)).all()

    all_tasks = [
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
            plan_in_days=x.plan_in_days,
            shift=x.shift,
            start_date=x.start_date,
            user_count_by_plan=x.user_count_by_plan,
        ).model_dump()
        for x in stmt
    ]
    all_scope_plan = 0
    plan = 0
    all_scope_done = 0
    for index in range(len(all_tasks)):
        delta = datetime.now() - all_tasks[index]["start_date"]
        plan += (all_tasks[index]["user_count_by_plan"] * all_tasks[index]["shift"]) * (
            delta.days
        )
        all_scope_plan += all_tasks[index]["plan_scope_hours"]
        all_scope_done += all_tasks[index]["done_scope"]

    diff = plan - all_scope_done
    plan_end_date = session.execute(
        select(Task).filter_by(object_id=id).order_by(Task.start_date.desc())
    ).scalar()
    return {
        "plan": plan / all_scope_plan * 100,
        "predict": plan_end_date.deadline + timedelta(hours=diff),
        "predict_in_hours": diff,
    }


def get_plan_date(id):
    from tasks import Task

    plan_start_date = session.execute(
        select(Task).filter_by(object_id=id).order_by(Task.start_date.asc())
    ).scalar()

    plan_end_date = session.execute(
        select(Task).filter_by(object_id=id).order_by(Task.start_date.desc())
    ).scalar()
    return {
        "start_date": plan_start_date.start_date,
        "end_date": plan_end_date.deadline,
    }


@object_api.route("/<id>/object_calc", methods=["GET"])
@validate()
def get_object_calc(id: uuid.UUID):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "object not found"}, 404)
    fact = calculate_fact(id)
    plan = calculate_plan_and_predict(id)
    dates = get_plan_date(id)
    return ({"fact": fact, "plan": plan, "dates": dates}, 200)
