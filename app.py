from flask import Flask, request, url_for
from datetime import datetime
from db import Base

app = Flask(__name__)

from object import object_api

app.register_blueprint(object_api, url_prefix="/objects")

from user import user_api

app.register_blueprint(user_api, url_prefix="/users")

from assignment import assignment_api

app.register_blueprint(assignment_api, url_prefix="/assignments")

from tasks import task_api

app.register_blueprint(task_api, url_prefix="/tasks")

from instruction import instruction_api

app.register_blueprint(instruction_api, url_prefix="/instructions")

from task_instructions import instruct_task_api

app.register_blueprint(instruct_task_api, url_prefix="/task_instructions")

from material import material_api

app.register_blueprint(material_api, url_prefix="/materials")

from task_materials import materials_task_api

app.register_blueprint(materials_task_api, url_prefix="/task_materials")

from user_tasks import user_task_api

app.register_blueprint(user_task_api, url_prefix="/user_tasks")

from obj_changes import changes_api

app.register_blueprint(changes_api, url_prefix="/changes")
