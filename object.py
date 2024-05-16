from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session



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
def create_object():
    data = request.json
    new_object = Object(name = data.get("name"))
    search = session.execute(select(Object).filter_by(name=new_object.name)).first()
    if search is None:
        session.add(new_object)
        session.commit()
        return (object_to_dict(new_object), 201)
    else:
        return ({'error':'object exists'},409)

@object_api.route("/")
def list_objects():
    q = select(Object)
    objects = session.scalars(q).all()
    new_dict = [object_to_dict(x) for x in objects]
    return new_dict

@object_api.route("/<id>")
def get_object(id):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (object_to_dict(search), 200)
    else:
        return ({'error':'object not found'},404)

@object_api.route("/<id>", methods=["DELETE"])
def delete_object(id):
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ('', 204)
    else:
        return ({'error':'object not found'},404)

@object_api.route("/<id>/users")
def get_users_from_object(id):
    from assignment import Assignment
    from user import User
    search = session.execute(select(Object).filter_by(id=id)).scalar_one_or_none()
    if search is None:
        return ({'error':'object not found'},404)
    users = session.scalars(select(User).join(Assignment).filter_by(object_id=id)).all()
    from user import user_to_dict
    return [user_to_dict(x) for x in users] 
        


