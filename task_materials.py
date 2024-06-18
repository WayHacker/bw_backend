from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate


class TaskMaterials(Base):
    __tablename__ = "task_materials"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("task.id"))
    material_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("material.id"))


class TaskMaterialsModuleOut(BaseModel):
    id: uuid.UUID
    description: str
    task_id: uuid.UUID
    material_id: uuid.UUID


class TaskMaterialsModuleIn(BaseModel):
    description: str
    task_id: uuid.UUID
    material_id: uuid.UUID


materials_task_api = Blueprint("task_materials", "task_materials")


@materials_task_api.route("/", methods=["POST"])
@validate()
def create_assignment(body: TaskMaterialsModuleIn):
    new_assignment = TaskMaterials(
        description=body.description,
        task_id=body.task_id,
        material_id=body.material_id,
    )
    session.add(new_assignment)
    session.commit()
    return (
        TaskMaterialsModuleOut(
            id=new_assignment.id,
            description=new_assignment.description,
            task_id=new_assignment.task_id,
            material_id=new_assignment.material_id,
        ).model_dump(),
        201,
    )


@materials_task_api.route("/", methods=["GET"])
@validate()
def list_assignments():
    q = select(TaskMaterials)
    assignments = session.scalars(q).all()
    # new_dict = [(x) for x in assignments]
    return [
        TaskMaterialsModuleOut(
            id=x.id,
            description=x.description,
            task_id=x.task_id,
            material_id=x.material_id,
        ).model_dump()
        for x in assignments
    ]


@materials_task_api.route("/<id>", methods=["GET"])
@validate()
def get_assignment(id: uuid.UUID):
    search = session.execute(
        select(TaskMaterials).filter_by(id=id)
    ).scalar_one_or_none()
    if search is not None:
        return (
            TaskMaterialsModuleOut(
                id=search.id,
                description=search.description,
                task_id=search.task_id,
                material_id=search.material_id,
            ).model_dump(),
            200,
        )
    else:
        return ({"error": "assignment not found"}, 404)


@materials_task_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_assignment(id: uuid.UUID):
    search = session.execute(
        select(TaskMaterials).filter_by(id=id)
    ).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "assignment not found"}, 404)
