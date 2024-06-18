from flask import Blueprint
from sqlalchemy import text, select
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


@task_api.route("/", methods=["POST"])
@validate()
def create_task(body: ModuleTaskIn):
    new_task = Task(description=body.description, deadline=body.deadline)
    session.add(new_task)
    session.commit()
    return (
        ModuleTaskOut(
            id=new_task.id, description=new_task.description, deadline=new_task.deadline
        ).model_dump(),
        201,
    )


@task_api.route("/", methods=["GET"])
@validate()
def list_tasks():
    q = select(Task)
    tasks = session.scalars(q).all()
    return [
        ModuleTaskOut(
            description=x.description, id=x.id, deadline=x.deadline
        ).model_dump()
        for x in tasks
    ]


@task_api.route("/<id>", methods=["GET"])
@validate()
def get_task(id: uuid.UUID):
    search = session.execute(select(Task).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (
            ModuleTaskOut(
                id=id, description=search.description, deadline=search.deadline
            ).model_dump(),
            200,
        )

    else:
        return ({"error": "task not found"}, 404)


@task_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_task(id: uuid.UUID):
    search = session.execute(select(Task).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "assignment not found"}, 404)


@task_api.route("/<id>/instructions", methods=["GET"])
@validate()
def get_instructions_from_task(id: uuid.UUID):
    from task_instructions import TaskInstructions
    from instruction import Instruction, InstrucModelOut

    search = session.execute(select(Task).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "task not found"}, 404)
    instructions = session.scalars(
        select(Instruction).join(TaskInstructions).filter_by(task_id=id)
    ).all()
    return [InstrucModelOut(id=x.id, name=x.name).model_dump() for x in instructions]


@task_api.route("/<id>/materials", methods=["GET"])
@validate()
def get_materials_from_task(id: uuid.UUID):
    from task_materials import TaskMaterials
    from material import Material, MaterialModelOut

    search = session.execute(select(Task).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({"error": "task not found"}, 404)
    materials = session.scalars(
        select(Material).join(TaskMaterials).filter_by(task_id=id)
    ).all()
    return [
        MaterialModelOut(id=x.id, name=x.name, supply=x.supply).model_dump()
        for x in materials
    ]
