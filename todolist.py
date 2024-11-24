class ToDoList:
    def __init__(self) -> None:
        self.todo = []

    def add(self,task_name):
        task_dict = {
            'task' : task_name,
            'id': len(self.todo),
            'completed' : False,
            'active' : True
        }
        return self.todo.append(task_dict)
    
    def remove(self,task_id):
        if task_id < len(self.todo):
            self.todo[task_id]["active"] = False
        else: 
            raise ValueError("Check the task id provided")
    
    def complete(self,task_id):
        if task_id < len(self.todo):
            self.todo[task_id]["completed"] = True
        else:
            raise ValueError("Check the task id provided")

    def incomplete(self,task_id):
        if task_id < len(self.todo):
            self.todo[task_id]["completed"] = False
        else:
            raise ValueError("Check the task id provided")

    def list(self):
        return self.todo

if __name__ == "__main__":
    todo = ToDoList()
    task1 = todo.add("Call me")
    task2 = todo.add("buy groceries")
    todo.remove(100)
    all_task = todo.list()

    print(all_task)