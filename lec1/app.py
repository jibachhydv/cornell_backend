# Importing flask
from flask import Flask
from flask import request


import json

# creating a flask object
app = Flask(__name__)

# todo list
tasks = {
    0: {
        "id":0,
        "description": "do laundary",
        "done": False
    },
    1: {
        "id":1,
        "description": "do homework",
        "done": False
    },
    2: {
        "id":2,
        "description": "visit home",
        "done": False
    }
}

tasks_id_counter = 2

# '/' routes
@app.route("/")
def hello():
    return "Hello World!"


@app.route("/tasks/")
def get_all_tasks():
    response = {
        "tasks": list(tasks.values())
    }

    return json.dumps(response)


@app.route("/tasks/", methods=['POST'])
def create_task():
    global tasks_id_counter
    body = json.loads(request.data)
    description = body.get("description", "none")

    response = {
        "id": tasks_id_counter,
        "description": description,
        "done": False
    }
    tasks[tasks_id_counter] = response
    tasks_id_counter+=1

    return json.dumps(response),201


@app.route("/tasks/<int:task_id>/")
def get_specific_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"error":"Task Not Found"}),404
    
    return json.dumps(task),200

@app.route("/tasks/<int:task_id>/",methods=['POST'])
def update_task(task_id):

    # check if task exists
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"error":"Task Not Found"}),404
    
    body = json.loads(request.data)
    print(body)
    description = body.get("description", task["description"])
    done = body.get("done",task["done"])

    task["description"] = description
    task["done"] = done

    return json.dumps(task),200

# delete the task
@app.route("/tasks/<int:task_id>/",methods=['DELETE'])
def delete_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"error": "Not Found"}), 404

    del tasks[task_id]
    return json.dumps({"message": "Task Deleted"}),200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)