import queue
import random
from enum import Enum
#Final project for query based task management system
#learn and practice/play with python and keep making cool stuff




class EmployeeStatus(Enum):
    FREE = "free"
    BUSY = "busy"

class ManagerQuery:
    def __init__(self, task_id, time_allotted, reward_point):
        self.task_id = task_id
        self.time_allotted = time_allotted
        self.reward_point = reward_point

class EmployeeQuery:
    def __init__(self, emp_id, task_id, time_taken):
        self.emp_id = emp_id
        self.task_id = task_id
        self.time_taken = time_taken

task_queue = queue.Queue()
employee_status = {
    "E1": EmployeeStatus.FREE,
    "E2": EmployeeStatus.FREE,
    "E3": EmployeeStatus.FREE
}

employee_task = {}
leader_board = []

def assign_work(employee, curr_work):
    employee_status[employee] = EmployeeStatus.BUSY
    employee_task[employee] = curr_work

def current_status():
    for employee, work in employee_task.items():
        task_id = work.task_id
        time_allot = work.time_allotted
        print(f"{employee} is working on: {task_id}, Expected time to complete: {time_allot}")

def update_changes(emp_obj):
    employee_status[emp_obj.emp_id] = EmployeeStatus.FREE
    employee_task[emp_obj.emp_id] = "No work"
    leader_board.append(emp_obj)

def display_leaderboard():
    print("Leaderboard:")
    print("{:<10} {:<10} {:<10}".format("Employee", "Task ID", "Time Taken"))
    for emp in leader_board:
        print("{:<10} {:<10} {:<10}".format(emp.emp_id, emp.task_id, emp.time_taken))

def add_employee(emp_id):
    if emp_id in employee_status:
        print(f"Employee {emp_id} already exists.")
    else:
        employee_status[emp_id] = EmployeeStatus.FREE
        print(f"Employee {emp_id} added successfully.")

def process_manager_input():
    input_manager = input("Task Id, Time Alloted, Reward Points: ")
    task_id, time_allotted, reward_point = [value.strip() for value in input_manager.split(',')]
    new_query = ManagerQuery(task_id, time_allotted, reward_point)
    task_queue.put(new_query)

    if not task_queue.empty():
        curr_work = task_queue.queue[0]
        free_employees = [employee_id for employee_id, status in employee_status.items() if status == EmployeeStatus.FREE]
        if free_employees:
            em_assigned = random.choice(free_employees)
            assign_work(em_assigned, curr_work)
            curr_work=task_queue.get()
        else:
            print("Right now, all employees are busy. Please wait for an employee query.")

def process_employee_input():
    employee_id = input("What is your ID: ")

    if employee_id not in employee_status:
        print("Invalid employee ID.")
        return

    if employee_status[employee_id] == EmployeeStatus.FREE:
        print("You are not assigned with any work.")
    else:
        task_id = ""
        for emp_id, work in employee_task.items():
            if emp_id == employee_id:
                task_id = work.task_id
                print("You have {} as a pending task. If you have completed it, kindly enter the time taken: ".format(task_id))
                time_taken = input()
                new_emp = EmployeeQuery(employee_id, task_id, time_taken)
                update_changes(new_emp)
                return

        print("Task not found for the given employee ID.")


def int_interface():
    while True:
        choice = input("Enter query (M for manager, E for employee, L for leaderboard, CS for Check_Status, A for add employee, Q to quit): ")
        
        if choice == 'M' or choice == 'm':
            process_manager_input()
        elif choice == 'E' or choice == 'e':
            process_employee_input()
        elif choice == 'L' or choice == 'l':
            display_leaderboard()
        elif choice == 'A' or choice == 'a':
            emp_id = input("Enter employee ID to add: ")
            add_employee(emp_id)
        elif choice == 'cs' or choice == 'CS':
            current_status()
        elif choice == 'Q' or choice == 'q':
            break
        else:
            print("Invalid query. Please try again.")

int_interface()
