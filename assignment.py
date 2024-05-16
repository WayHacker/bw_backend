from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session



class Assignment(Base):
    __tablename__ = "assignment"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    object_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("object.id"))

def assignment_to_dict(obj):
    return {"id": obj.id, "description": obj.description, "user_id": obj.user_id, "object_id": obj.object_id}


assignment_api = Blueprint("assignments", "assignments")

@assignment_api.route("/", methods=["POST"])
def create_assignment():
    data = request.json
    new_assignment = Assignment(description = data.get('description'), user_id = data.get('user_id'), object_id = data.get('object_id'))    
    session.add(new_assignment)
    session.commit()
    return (assignment_to_dict(new_assignment), 201)

@assignment_api.route("/")
def list_assignments():
    q = select(Assignment)
    assignments = session.scalars(q).all()
    new_dict = [assignment_to_dict(x) for x in assignments]
    return new_dict

@assignment_api.route("/<id>")
def get_assignment(id):
    search = session.execute(select(Assignment).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (assignment_to_dict(search), 200)
    else:
        return ({'error':'assignment not found'},404)

@assignment_api.route("/<id>", methods=["DELETE"])
def delete_assignment(id):
    search = session.execute(select(Assignment).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ('', 204)
    else:
        return ({'error':'assignment not found'},404)



