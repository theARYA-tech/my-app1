import tasks
from datetime import datetime

task_list = tasks.load_tasks()


while True:
    print("\n1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Mark Task Completed")
    print("5. Exit")

    choice = input("Choose: ")

    if choice == "1":
        task = input("Enter task: ")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        task_list.append({
          "task": task,
          "time": timestamp,
          "done": False
        })
        
        tasks.save_tasks(task_list)
        
    elif choice == "2":

     if not task_list:
        print("No tasks yet.")

     else:
        for i, t in enumerate(task_list, 1):

            status = "√" if t["done"] else "X"

            print(f"{i} - {t['task']} ({t['time']}) [{status}]")

    elif choice == "3":
        number = int(input("Enter task number to remove: "))
        task_list.pop(number - 1)
        tasks.save_tasks(task_list)

    elif choice == "4":
     number = int(input("Enter task number completed: "))
     if 1 <= number <= len(task_list):
        task_list[number - 1]["done"] = True
        tasks.save_tasks(task_list)
        print("Task marked as completed.")
     else:
        print("Invalid task number.")

    elif choice == "5":
     break    