from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[Optional[str]]
    phone: Mapped[str]


class UserModelOut(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    phone: str


class UserModelIn(BaseModel):
    phone: str
    name: Optional[str]


user_api = Blueprint("users", "users")


@user_api.route("/", methods=["POST"])
@validate()
def create_user(body: UserModelIn):
    new_user = User(name=body.name, phone=body.phone)
    search = session.execute(select(User).filter_by(phone=new_user.phone)).first()
    if search is None:
        session.add(new_user)
        session.commit()
        return (
            UserModelOut(
                name=new_user.name, phone=new_user.phone, id=new_user.id
            ).model_dump(),
            201,
        )
    else:
        return ({"error": "user exists"}, 409)


@user_api.route("/")
@validate()
def list_users():
    q = select(User)
    users = session.scalars(q).all()
    return [
        UserModelOut(name=x.name, phone=x.phone, id=x.id).model_dump() for x in users
    ]


@user_api.route("/<id>")
@validate()
def get_user(id: uuid.UUID):
    search = session.execute(select(User).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return UserModelOut(name=search.name, id=search.id, phone=search.phone)
    else:
        return ({"error": "user not found"}, 404)


@user_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_user(id: uuid.UUID):
    search = session.execute(select(User).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "user not found"}, 404)
