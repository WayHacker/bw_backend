from flask import request, Blueprint, send_file
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel, Field
from flask_pydantic import validate
from io import BytesIO


class Material(Base):
    __tablename__ = "material"
    # maybe add description column
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[Optional[str]]
    reciept: Mapped[bytes]
    supply: Mapped[bool]


class MaterialModelOut(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    supply: bool


material_api = Blueprint("materials", "materials")


@material_api.route("/", methods=["POST"])
def upload_material():
    file = request.files["file"]
    if request.form["supply"] == "True":
        new_file = Material(name=file.filename, supply=True, reciept=file.read())
        session.add(new_file)
        session.commit()
        return (
            MaterialModelOut(
                name=new_file.name, id=new_file.id, supply=new_file.supply
            ).model_dump(),
            201,
        )
    elif request.form["supply"] == "False":
        new_file = Material(name=file.filename, supply=False, reciept=file.read())
        session.add(new_file)
        session.commit()
        return (
            MaterialModelOut(
                name=new_file.name, id=new_file.id, supply=new_file.supply
            ).model_dump(),
            201,
        )


@material_api.route("/", methods=["GET"])
@validate()
def list_material():
    q = select(Material)
    instructions = session.scalars(q).all()
    return [
        MaterialModelOut(name=x.name, id=x.id, supply=x.supply).model_dump()
        for x in instructions
    ]


@material_api.route("/<id>", methods=["GET"])
@validate()
def get_material(id: uuid.UUID):
    search = session.execute(select(Material).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (
            MaterialModelOut(
                name=search.name, id=id, supply=search.supply
            ).model_dump(),
            200,
        )
    else:
        return ({"error": "material not found"}, 404)


@material_api.route("/<id>", methods=["GET"])
@validate()
def download_file(id: uuid.UUID):
    file = session.execute(select(Material).filter_by(id=id)).scalar_one_or_none()
    if file is not None:
        return send_file(
            BytesIO(file.pdf_file),
            download_name=file.name,
            as_attachment=True,
        )
    else:
        return ({"error": "object not found"}, 404)


@material_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_material(id: uuid.UUID):
    search = session.execute(select(Material).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "file not found"}, 404)


@material_api.route("/<id>", methods=["PATCH"])
@validate()
def switch_supply(id: uuid.UUID):
    search = session.execute(select(Material).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        if search.supply is True:
            search.supply = False
            session.add(search)
            session.commit()
            return ("", 204)

        search.supply = True
        session.add(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "material not found"}, 404)
