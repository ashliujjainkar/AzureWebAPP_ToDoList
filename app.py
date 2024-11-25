from flask import Flask, request, jsonify
from todolist import ToDoList
from pymongo import MongoClient
from bson import ObjectId
import os


app = Flask(__name__)

version_file_path = os.path.join(os.getcwd(), "version.txt")
api_version = "0.0"
if os.path.exists(version_file_path):
    with open(version_file_path, "r") as f:
        api_version = f.read()
print("API Version:", api_version)

cosmosdb_uri = os.environ.get('COSMOSDB_URI')
client = MongoClient(cosmosdb_uri)
db = client['tododb']
tasks_collection = db['tasks']

def task_serializer(task):
    return {
        'id': str(task['id']),  
        'task': task['task'],
        'completed': task['completed']
    }

@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({"version": api_version})

@app.route('/', methods=['GET'])
def get_home():
    return "Hello! Welcome to Todo List App"

@app.route('/list', methods=['GET'])
def list_tasks():
    tasks = list(tasks_collection.find({}))
    return jsonify([task_serializer(task) for task in tasks])

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.json.get('task')
    # print("New task:",new_task, flush=True)
    if new_task:
        task_id = tasks_collection.count_documents({})+1
        task = {'id':task_id, 'task': new_task, 'completed': False} 
        tasks_collection.insert_one(task)
        # print("Task ID:",task['id'], flush=True) 
        return jsonify(task_serializer(task)), 201
    return jsonify({"error": "No task provided"}), 400

@app.route('/complete', methods=['POST'])
def complete_task():
    task_id = request.json.get('id')
    task = tasks_collection.find_one({"id": task_id})  
    if task:
        tasks_collection.update_one({"id": task_id}, {"$set": {"completed": True}})
        task['completed'] = True
        return jsonify(task_serializer(task))
    return jsonify({"error": "Task not found"}), 404

@app.route('/incomplete', methods=['POST'])
def incomplete_task():
    task_id = request.json.get('id')
    task = tasks_collection.find_one({"id": task_id})  
    if task:
        tasks_collection.update_one({"id": task_id}, {"$set": {"completed": False}})
        task['completed'] = False
        return jsonify(task_serializer(task))
    return jsonify({"error": "Task not found"}), 404

@app.route('/dump', methods=['GET'])
def dump():
    tasks = list(tasks_collection.find({}, {'_id': 0}))
    return jsonify({"message": f"{len(tasks)} tasks stored in Cosmos DB"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)