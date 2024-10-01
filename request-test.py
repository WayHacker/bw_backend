import requests


r = requests.post("http://127.0.0.1:5000/objects/", json={"name": "Самокатная 21"})

alpha_id = r.json().get("id")


# r = requests.post(
#     "http://127.0.0.1:5000/tasks/",
#     json={
#         "user_count_by_plan":3,
#         "description": "Eat mentos",
#         "plan_per_hour": 10,
#         "shift": 8,
#         "work_scope": 200,
#         "object_id": alpha_id,
#         "start_date": "2024-10-12 08:00:00",
#     },
# )
# r = requests.post(
#     "http://127.0.0.1:5000/tasks/",
#     json={
#         "user_count_by_plan": 1,
#         "description": "Poop",
#         "plan_per_hour": 10,
#         "shift": 10,
#         "work_scope": 10,
#         "done_scope": 10,
#         "object_id": alpha_id,
#         "start_date": "2024-09-09 08:00:00",
#     },
# )

print(r.status_code)
r = requests.post(
    "http://127.0.0.1:5000/tasks/",
    json={
        "user_count_by_plan": 1,
        "description": "Drink Cock-Cola",
        "plan_per_hour": 10,
        "shift": 10,
        "work_scope": 10,
        "object_id": alpha_id,
        "done_scope": 20,
        "start_date": "2024-09-02 08:00:00",
    },
)

cola_task = r.json().get("id")
print(r.json())

r = requests.post(
    "http://127.0.0.1:5000/users/",
    json={"name": "Max", "phone": "+78889990011", "role": "prorab"},
)
print(r.status_code)
print(r.json())
max_id = r.json().get("id")
r = requests.post(
    "http://127.0.0.1:5000/assignments/",
    json={
        "description": "Max working on Alpha",
        "user_id": max_id,
        "object_id": alpha_id,
    },
)
print(r.json())
r = requests.post(
    "http://127.0.0.1:5000/users/",
    json={"name": "Jumaysenba", "phone": "+77777777777", "role": "worker"},
)
print(r.status_code)
worker_id = r.json().get("id")
r = requests.post(
    "http://127.0.0.1:5000/assignments/",
    json={
        "description": "Jumaysenba working on Alpha",
        "user_id": worker_id,
        "object_id": alpha_id,
    },
)
r = requests.post(
    "http://127.0.0.1:5000/users/", json={"name": "Gandon", "phone": "+71112223344", "role":"worker"}
)
print(r.status_code)
worker_id = r.json().get("id")
r = requests.post(
    "http://127.0.0.1:5000/assignments/",
    json={
        "description": "Gandon working on Alpha",
        "user_id": worker_id,
        "object_id": alpha_id,
    },
)

r = requests.post(
    "http://127.0.0.1:5000/user_tasks/",
    json={
        "description": "Max working on this task",
        "task_id": cola_task,
        "user_id": max_id,
    },
)
print(r.status_code)


r = requests.post(
    "http://127.0.0.1:5000/changes/",
    json={
        "name": "First change",
        "who_change": max_id,
        "reasons": "Some reasons",
        "object_id": alpha_id,
    },
)
print(r.status_code)

# r = requests.put(
#     "http://127.0.0.1:5000/tasks/",
#     json={
#         "task_id": cola_task,
#         "user_count_by_plan": 1,
#         "description": "Drink Cock-Cola",
#         "plan_per_hour": 10,
#         "shift": 10,
#         "work_scope": 10,
#         "object_id": alpha_id,
#         "done_scope": 40,
#         "start_date": "2024-09-02 08:00:00",
#     },
# )
# print(r.status_code)
