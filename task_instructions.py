from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate


class TaskInstructions(Base):
    __tablename__ = "task_instructions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("task.id"))
    instruction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instruction.id"))


class TaskInstrucModuleOut(BaseModel):
    id: uuid.UUID
    description: str
    task_id: uuid.UUID
    instruction_id: uuid.UUID


class TaskInstrucModuleIn(BaseModel):
    description: str
    task_id: uuid.UUID
    instruction_id: uuid.UUID


instruct_task_api = Blueprint("task_instructions", "task_instructions")


@instruct_task_api.route("/", methods=["POST"])
@validate()
def create_assignment(body: TaskInstrucModuleIn):
    new_assignment = TaskInstructions(
        description=body.description, task_id=body.task_id, instruction_id=body.instruction_id
    )
    session.add(new_assignment)
    session.commit()
    return (
        TaskInstrucModuleOut(
            id=new_assignment.id,
            description=new_assignment.description,
            task_id=new_assignment.task_id,
            instruction_id=new_assignment.instruction_id,
        ).model_dump(),
        201,
    )


@instruct_task_api.route("/", methods=["GET"])
@validate()
def list_assignments():
    q = select(TaskInstructions)
    assignments = session.scalars(q).all()
    # new_dict = [(x) for x in assignments]
    return [
        TaskInstrucModuleOut(
            id=x.id,
            description=x.description,
            task_id=x.task_id,
            instruction_id=x.instruction_id,
        ).model_dump()
        for x in assignments
    ]


@instruct_task_api.route("/<id>", methods=["GET"])
@validate()
def get_assignment(id: uuid.UUID):
    search = session.execute(
        select(TaskInstructions).filter_by(id=id)
    ).scalar_one_or_none()
    if search is not None:
        return (
            TaskInstrucModuleOut(
                id=search.id,
                description=search.description,
                task_id=search.task_id,
                instruction_id=search.instruction_id,
            ).model_dump(),
            200,
        )
    else:
        return ({"error": "assignment not found"}, 404)


@instruct_task_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_assignment(id: uuid.UUID):
    search = session.execute(
        select(TaskInstructions).filter_by(id=id)
    ).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "assignment not found"}, 404)
