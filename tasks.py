from flask import Blueprint
from sqlalchemy import text, select, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from db import Base, session
from pydantic import BaseModel
from flask_pydantic import validate
from typing import Optional
import datetime


class Task(Base):
    __tablename__ = "task"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    deadline: Mapped[datetime.datetime]
    work_scope: Mapped[int]
    done_scope: Mapped[int]
    object_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("object.id"))



class ModuleTaskIn(BaseModel):
    done_scope: Optional[int] = 0 
    work_scope: int
    object_id: uuid.UUID
    description: str
    deadline: datetime.datetime


class ModuleTaskOut(BaseModel):
    id: uuid.UUID
    description: str
    deadline: datetime.datetime
    work_scope: int
    object_id: uuid.UUID
    done_scope: int


task_api = Blueprint("tasks", "tasks")


@task_api.route("/", methods=["POST"])
@validate()
def create_task(body: ModuleTaskIn):
    from object import Object

    search = session.execute(select(Object).filter_by(id=body.object_id)).first()
    if search is None:
        return ({"error": "object not found"}, 404)
    new_task = Task(
        description=body.description,
        deadline=body.deadline,
        work_scope=body.work_scope,
        done_scope=body.done_scope,
        object_id=body.object_id,
    )
    session.add(new_task)
    session.commit()
    return (
        ModuleTaskOut(
            id=new_task.id,
            description=new_task.description,
            deadline=new_task.deadline,
            work_scope=new_task.work_scope,
            object_id=new_task.object_id,
            done_scope=new_task.done_scope,
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
            description=x.description,
            id=x.id,
            deadline=x.deadline,
            work_scope=x.work_scope,
            object_id=x.object_id,
            done_scope=x.done_scope,
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
