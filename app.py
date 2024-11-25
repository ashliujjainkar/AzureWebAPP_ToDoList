from flask import Flask,request, jsonify
import os

app = Flask(__name__)

version_file_path = os.path.join(os.getcwd(), 'version.txt')
api_version = "0.0"
if os.path.exists(version_file_path):
    with open(version_file_path, 'r') as f:
        api_version = f.read()
print("API Version:", api_version)

tasks = {}
task_counter = 1

def task_serializer(task):
    return{
        'id': task['id'],
        'task': task['task'],
        'completed': task['completed']
    }

@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({"version": api_version})

@app.route('/', methods=['GET'])
def get_home():
    return "Hello! Welcome to Todo List App"


@app.route('/list',methods = ['GET'])
def list_tasks():
    return jsonify([task_serializer(task) for task in tasks.values()])

@app.route('/add',methods = ['POST'])
def add_task():
    global task_counter
    new_task = request.json.get('task')
    if new_task:
        task = {'id': task_counter,'task': new_task, 'completed': False}
        tasks[task_counter] = task
        task_counter += 1
        return jsonify(task_serializer(task)), 201
    return jsonify({"error":"No task Provided"}), 400

@app.route('/complete', methods=['POST'])
def complete_task():
    task_id = request.json.get('id')
    task = tasks.get(task_id)
    if task:
        task['completed'] = True
        return jsonify(task_serializer(task))
    return jsonify({"error":"Task not Found"}),404

@app.route('/incomplete',methods=['POST'])
def incomplete():
    task_id = request.json.get('id')
    task = tasks.get(task_id)
    if task:
        task['completed'] = False
        return jsonify(task_serializer(task))
    return jsonify({"error":"Task not Found"}),404

@app.route('/dump', methods=['GET'])
def dump():
    return jsonify({"message":f"{len(tasks)} tasks stored in memory"})

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=8888)