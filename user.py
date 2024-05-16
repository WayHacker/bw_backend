from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session


class User(Base):
    __tablename__ = "employee"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[Optional[str]]
    phone: Mapped[str]




def user_to_dict(obj):

    return {"id": obj.id, "name": obj.name, "phone": obj.phone}


user_api = Blueprint("users", "users")


@user_api.route("/", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(name = data.get('name'), phone = data.get('phone'))
    search = session.execute(select(User).filter_by(name=new_user.name)).first()
    if search is None:
        session.add(new_user)
        session.commit()
        return (user_to_dict(new_user), 201)
    else:
        return ({'error':'user exists'},409)

@user_api.route("/")
def list_users():
    q = select(User)
    users = session.scalars(q).all()
    new_dict = [user_to_dict(x) for x in users]
    return new_dict

@user_api.route("/<id>")
def get_user(id):
    search = session.execute(select(User).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (user_to_dict(search), 200)
    else:
        return ({'error':'user not found'},404)

@user_api.route("/<id>", methods=["DELETE"])
def delete_user(id):
    search = session.execute(select(User).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ('', 204)
    else:
        return ({'error':'user not found'},404)



