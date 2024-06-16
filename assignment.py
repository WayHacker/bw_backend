from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate


class Assignment(Base):
    __tablename__ = "assignment"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    object_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("object.id"))


class AssignmentModuleOut(BaseModel):
    id: uuid.UUID
    description: str
    user_id: uuid.UUID
    object_id: uuid.UUID


class AssignmentModuleIn(BaseModel):
    description: str
    user_id: uuid.UUID
    object_id: uuid.UUID


class AssignmentList(BaseModel):
    root: List[AssignmentModuleOut]


assignment_api = Blueprint("assignments", "assignments")


@assignment_api.route("/", methods=["POST"])
@validate()
def create_assignment(body: AssignmentModuleIn):
    new_assignment = Assignment(
        description=body.description, user_id=body.user_id, object_id=body.object_id
    )
    session.add(new_assignment)
    session.commit()
    return (
        AssignmentModuleOut(
            id=new_assignment.id,
            description=new_assignment.description,
            user_id=new_assignment.user_id,
            object_id=new_assignment.object_id,
        ).model_dump(),
        201,
    )


@assignment_api.route("/", methods=["GET"])
@validate()
def list_assignments():
    q = select(Assignment)
    assignments = session.scalars(q).all()
    # new_dict = [(x) for x in assignments]
    return [
        AssignmentModuleOut(
            id=x.id,
            description=x.description,
            user_id=x.user_id,
            object_id=x.object_id,
        ).model_dump()
        for x in assignments
    ]


@assignment_api.route("/<id>", methods=["GET"])
@validate()
def get_assignment(id: uuid.UUID):
    search = session.execute(select(Assignment).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (
            AssignmentModuleOut(
                id=search.id,
                description=search.description,
                user_id=search.user_id,
                object_id=search.object_id,
            ).model_dump(),
            200,
        )

    else:
        return ({"error": "assignment not found"}, 404)


@assignment_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_assignment(id: uuid.UUID):
    search = session.execute(select(Assignment).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "assignment not found"}, 404)
