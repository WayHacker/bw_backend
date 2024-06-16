from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate


class AssignmentTask(Base):
    __tablename__ = "assignment_task"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("task.id"))
    object_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("object.id"))


class AssignmentTaskModuleOut(BaseModel):
    id: uuid.UUID
    description: str
    task_id: uuid.UUID
    object_id: uuid.UUID


class AssignmentTaskModuleIn(BaseModel):
    description: str
    task_id: uuid.UUID
    object_id: uuid.UUID


class AssignmentTaskList(BaseModel):
    root: List[AssignmentTaskModuleOut]


assignment_task_api = Blueprint("assignments_tasks", "assignments_tasks")


@assignment_task_api.route("/", methods=["POST"])
@validate()
def create_assignment_task(body: AssignmentTaskModuleIn):
    new_assignment = AssignmentTask(
        description=body.description, task_id=body.task_id, object_id=body.object_id
    )
    session.add(new_assignment)
    session.commit()
    return (
        AssignmentTaskModuleOut(
            id=new_assignment.id,
            description=new_assignment.description,
            task_id=new_assignment.task_id,
            object_id=new_assignment.object_id,
        ).model_dump(),
        201,
    )


@assignment_task_api.route("/", methods=["GET"])
@validate()
def list_assignments_tasks():
    q = select(AssignmentTask)
    assignments = session.scalars(q).all()
    # new_dict = [(x) for x in assignments]
    return [
        AssignmentTaskModuleOut(
            id=x.id,
            description=x.description,
            task_id=x.task_id,
            object_id=x.object_id,
        ).model_dump()
        for x in assignments
    ]


@assignment_task_api.route("/<id>", methods=["GET"])
@validate()
def get_assignment_task(id: uuid.UUID):
    search = session.execute(select(AssignmentTask).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (
            AssignmentTaskModuleOut(
                id=search.id,
                description=search.description,
                task_id=search.user_id,
                object_id=search.object_id,
            ).model_dump(),
            200,
        )

    else:
        return ({"error": "assignment not found"}, 404)


@assignment_task_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_assignment_task(id: uuid.UUID):
    search = session.execute(select(AssignmentTask).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "assignment not found"}, 404)
