import requests

base_url = "https://2dolist-hxe9gdbsd2e4fbeb.centralindia-01.azurewebsites.net"

def test_add_task():
    url = f"{base_url}/add"
    load = {
        "task":"Test task"
    }

    response = requests.post(url,json=load)
    assert response.status_code == 201, "Failed to add task"

    response_data = response.json()
    assert "task" in response_data
    assert response_data["task"] == load["task"]
    assert response_data["completed"] is False

def test_list_task():
    url = f"{base_url}/list"

    response = requests.get(url)
    assert response.status_code == 200, "Failed to list task"

    response_data = response.json()
    assert isinstance(response_data,list)
    if response_data:
        assert "task" in response_data[0]
        assert "completed" in response_data[0]

def test_dump_task():
    url = f"{base_url}/dump"

    response = requests.get(url)
    assert response.status_code == 200, "Failed to dump task"

    response_data = response.json()
    assert "message" in response_data

def test_version():
    url = f"{base_url}/version"

    response = requests.get(url)
    assert response.status_code == 200 , "Failed to get the version"

    response_data = response.json()
    assert "version" in response_data

def test_complete_task():
    add_url = f"{base_url}/add"
    load = {
        "task":"test task"
    }
    
    response = requests.post(add_url, json=load)
    assert response.status_code == 201, "failed to add test task"

    task = response.json()
    task_id = task["id"]

    complete_url = f"{base_url}/complete"
    complete_load = {
        "id": task_id
    }
    response = requests.post(complete_url, json=complete_load) 
    assert response.status_code == 200, "Failed to complete task"
    response_data = response.json()
    assert response_data["completed"] is True, "Task was not marked as completed"
    assert response_data["task"] == load["task"], "Task description does not match"

def test_incomplete_task():
    add_url = f"{base_url}/add"
    load = {
        "task" : "test task"
    }

    response = requests.post(add_url, json = load)
    assert response.status_code == 201, "failed to add test task"

    task = response.json()
    task_id = task["id"]

    incomplete_url = f"{base_url}/incomplete"
    incomplete_load = {
        "id" : task_id
    }

    response = requests.post(incomplete_url, json=incomplete_load)
    assert response.status_code == 200, "Fail to mark the task incomplete" 
    response_data = response.json()
    assert response_data["completed"] is False, "Task was not marked incomplete"
    assert response_data["task"] == load["task"], "Task description does not match"