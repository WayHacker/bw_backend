from flask import request, Blueprint
from sqlalchemy import text, select, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from db import Base, session
from pydantic import BaseModel
from flask_pydantic import validate
import datetime


class Task(Base):
    __tablename__ = "task"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    deadline: Mapped[datetime.datetime]


class ModuleTaskIn(BaseModel):
    description: str
    deadline: datetime.datetime


class ModuleTaskOut(BaseModel):
    id: uuid.UUID
    description: str
    deadline: datetime.datetime


task_api = Blueprint("tasks", "tasks")


def task_to_dict(obj):

    return {"id": obj.id, "description": obj.description, "deadline": obj.deadline}


@task_api.route("/", methods=["POST"])
@validate()
def create_assignment(body: ModuleTaskIn):
    new_task = Task(description=body.description, deadline=body.deadline)
    session.add(new_task)
    session.commit()
    return (
        ModuleTaskOut(
            id=new_task.id, description=new_task.description, deadline=new_task.deadline
        ),
        201,
    )


@task_api.route("/")
def list_assignments():
    q = select(Task)
    assignments = session.scalars(q).all()
    new_dict = [task_to_dict(x) for x in assignments]
    return new_dict


@task_api.route("/<id>")
def get_assignment(id):
    search = session.execute(select(Task).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (task_to_dict(search), 200)
    else:
        return ({"error": "assignment not found"}, 404)


@task_api.route("/<id>", methods=["DELETE"])
def delete_assignment(id):
    search = session.execute(select(Task).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "assignment not found"}, 404)
