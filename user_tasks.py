from flask import request, Blueprint
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, text, select, and_, update
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from db import Base, session
from pydantic import BaseModel
from flask_pydantic import validate


class UserTask(Base):
    __tablename__ = "user_task"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    description: Mapped[str]
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("task.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))


class UserTaskModuleOut(BaseModel):
    id: uuid.UUID
    description: str
    task_id: uuid.UUID
    user_id: uuid.UUID


class UserTaskModuleIn(BaseModel):
    description: str
    task_id: uuid.UUID
    user_id: uuid.UUID


user_task_api = Blueprint("user_tasks", "user_tasks")


@user_task_api.route("/", methods=["POST"])
@validate()
def create_assignment(body: UserTaskModuleIn):
    from assignment import Assignment
    from tasks import Task

    # select * from task join assignment on task.object_id=assignment.object_id
    # where task.id = 'de5a718a-0f3f-4b17-bd4f-54b6c8b4e80f';
    search = session.execute(
        select(Task)
        .join(Assignment, Task.object_id == Assignment.object_id)
        .where(Task.id == body.task_id)
    ).scalar_one_or_none()
    if search is None:
        return {"Error": "Task and user not in the same object!"}
    new_assignment = UserTask(
        description=body.description, task_id=body.task_id, user_id=body.user_id
    )
    session.add(new_assignment)
    session.commit()

    stmt = (
        update(Task)
        .where(body.task_id == Task.id)
        .values(user_count=Task.user_count + 1)
    )
    session.execute(stmt)
    session.commit()
    return (
        UserTaskModuleOut(
            id=new_assignment.id,
            description=new_assignment.description,
            task_id=new_assignment.task_id,
            user_id=new_assignment.user_id,
        ).model_dump(),
        201,
    )


@user_task_api.route("/", methods=["GET"])
@validate()
def list_assignments():
    q = select(UserTask)
    assignments = session.scalars(q).all()
    # new_dict = [(x) for x in assignments]
    return [
        UserTaskModuleOut(
            id=x.id,
            description=x.description,
            task_id=x.task_id,
            user_id=x.user_id,
        ).model_dump()
        for x in assignments
    ]


@user_task_api.route("/<id>", methods=["GET"])
@validate()
def get_assignment(id: uuid.UUID):
    search = session.execute(select(UserTask).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        return (
            UserTaskModuleOut(
                id=search.id,
                description=search.description,
                task_id=search.task_id,
                user_id=search.user_id,
            ).model_dump(),
            200,
        )
    else:
        return ({"error": "assignment not found"}, 404)


@user_task_api.route("/<id>", methods=["DELETE"])
@validate()
def delete_assignment(id: uuid.UUID):
    search = session.execute(select(UserTask).filter_by(id=id)).scalar_one_or_none()
    if search is not None:
        session.delete(search)
        session.commit()
        return ("", 204)
    else:
        return ({"error": "assignment not found"}, 404)
