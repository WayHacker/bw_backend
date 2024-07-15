from flask import request, Blueprint
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
    from user import User

    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "object not found"}, 404)
    users = session.scalars(select(User).join(Assignment).filter_by(object_id=id)).all()
    from user import user_to_dict

    return [user_to_dict(x) for x in users]


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
            id=x.id,
            description=x.description,
            deadline=x.deadline,
            work_scope=x.work_scope,
            object_id=x.object_id,
            done_scope=x.done_scope,
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
            id=x.id,
            description=x.description,
            deadline=x.deadline,
            work_scope=x.work_scope,
            object_id=x.object_id,
            done_scope=x.done_scope,
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
            id=x.id,
            description=x.description,
            deadline=x.deadline,
            work_scope=x.work_scope,
            object_id=x.object_id,
            done_scope=x.done_scope,
        ).model_dump()
        for x in tasks
    ]


@object_api.route("/<id>/fact", methods=["GET"])
@validate()
def calculate_fact(id: uuid.UUID):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "object not found"}, 404)
    from tasks import Task, ModuleTaskOut

    stmt = session.scalars(
        select(Task).where(
            and_(id == Task.object_id, Task.done_scope == Task.work_scope)
        )
    ).all()
    done_tasks = len(
        [
            ModuleTaskOut(
                id=x.id,
                description=x.description,
                deadline=x.deadline,
                work_scope=x.work_scope,
                object_id=x.object_id,
                done_scope=x.done_scope,
            ).model_dump()
            for x in stmt
        ]
    )

    stmt = session.scalars(select(Task).filter_by(object_id=id)).all()

    all_tasks = len(
        [
            ModuleTaskOut(
                id=x.id,
                description=x.description,
                deadline=x.deadline,
                work_scope=x.work_scope,
                object_id=x.object_id,
                done_scope=x.done_scope,
            ).model_dump()
            for x in stmt
        ]
    )
    return {"shit": done_tasks / all_tasks * 100}
