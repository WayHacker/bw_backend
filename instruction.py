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


class Instruction(Base):
    __tablename__ = "instruction"
    # maybe add description column
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[Optional[str]]
    # rename pdf_file to data
    pdf_file: Mapped[bytes] 


class InstrucModelOut(BaseModel):
    id: uuid.UUID
    name: Optional[str]


class InstrucModelIn(BaseModel):
    name: Optional[str]
    pdf_file: bytes


instruction_api = Blueprint("instructions", "instructions")


@instruction_api.route("/", methods=["POST"])
def create_instruction():
    file = request.files["file"]
    new_file = Instruction(name=file.filename, pdf_file=file.read())
    session.add(new_file)
    session.commit()
    return InstrucModelOut(name=new_file.name, id=new_file.id).model_dump(), 201


@instruction_api.route("/", methods=["GET"])
@validate()
def list_instructions():
    q = select(Instruction)
    instructions = session.scalars(q).all()
    return [InstrucModelOut(name=x.name, id=x.id).model_dump() for x in instructions]


@instruction_api.route("/<id>", methods=["GET"])
@validate()
def get_instruction(id: uuid.UUID):
    search = session.execute(select(Instruction).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return InstrucModelOut(name=search.name, id=id).model_dump(), 200
    else:
        return ({"error": "instruction not found"}, 404)


@instruction_api.route("/<id>", methods=["GET"])
@validate()
def download_file(id: uuid.UUID):
    file = session.execute(select(Instruction).filter_by(id=id)).scalar_one_or_none()
    if file is not None:
        return send_file(
            BytesIO(file.pdf_file),
            download_name=file.name,
            as_attachment=True,
        )
    else:
        return ({"error": "object not found"}, 404)


@instruction_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_object(id: uuid.UUID):
    search = session.execute(select(Instruction).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "file not found"}, 404)
