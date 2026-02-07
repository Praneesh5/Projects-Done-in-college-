import tkinter as tk
from tkinter import messagebox

# Employee Node
class Employee:
    def __init__(self, emp_id, name, rank, salary):
        self.id = emp_id
        self.name = name
        self.rank = rank
        self.salary = salary
        self.left = None
        self.right = None

# BST Class
class EmployeeBST:
    def __init__(self):
        self.root = None

    def insert(self, root, emp):
        if root is None:
            return emp
        if emp.id < root.id:
            root.left = self.insert(root.left, emp)
        elif emp.id > root.id:
            root.right = self.insert(root.right, emp)
        else:
            messagebox.showerror("Error", "Duplicate Employee ID")
        return root

    def insert_employee(self, emp_id, name, rank, salary):
        emp = Employee(emp_id, name, rank, salary)
        self.root = self.insert(self.root, emp)

    def search(self, root, emp_id):
        if root is None or root.id == emp_id:
            return root
        if emp_id < root.id:
            return self.search(root.left, emp_id)
        return self.search(root.right, emp_id)

    # Traversals
    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(f"{root.id} | {root.name} | {root.rank} | {root.salary}")
            self.inorder(root.right, result)

    def preorder(self, root, result):
        if root:
            result.append(f"{root.id} | {root.name} | {root.rank} | {root.salary}")
            self.preorder(root.left, result)
            self.preorder(root.right, result)

    def postorder(self, root, result):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(f"{root.id} | {root.name} | {root.rank} | {root.salary}")

# App Logic
bst = EmployeeBST()

def insert_employee():
    try:
        bst.insert_employee(
            int(id_entry.get()),
            name_entry.get(),
            rank_entry.get(),
            float(salary_entry.get())
        )
        messagebox.showinfo("Success", "Employee Inserted")
        clear_fields()
    except:
        messagebox.showerror("Error", "Invalid Input")

def search_employee():
    try:
        emp = bst.search(bst.root, int(id_entry.get()))
        if emp:
            messagebox.showinfo(
                "Employee Found",
                f"Name: {emp.name}\nRank: {emp.rank}\nSalary: {emp.salary}"
            )
        else:
            messagebox.showinfo("Result", "Employee Not Found")
    except:
        messagebox.showerror("Error", "Enter valid ID")

def show_inorder():
    result = []
    bst.inorder(bst.root, result)
    show_output("In-order Traversal", result)

def show_preorder():
    result = []
    bst.preorder(bst.root, result)
    show_output("Pre-order Traversal", result)

def show_postorder():
    result = []
    bst.postorder(bst.root, result)
    show_output("Post-order Traversal", result)

def show_output(title, data):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, title + "\n" + "-"*40 + "\n")
    for emp in data:
        output_box.insert(tk.END, emp + "\n")

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    rank_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

# GUI Layout
root = tk.Tk()
root.title("Employee Database Application")
root.geometry("520x500")

tk.Label(root, text="Employee Database Application",
         font=("Arial", 14, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

labels = ["Employee ID", "Name", "Rank", "Salary"]
for i, text in enumerate(labels):
    tk.Label(frame, text=text).grid(row=i, column=0, padx=5, pady=5)

id_entry = tk.Entry(frame)
name_entry = tk.Entry(frame)
rank_entry = tk.Entry(frame)
salary_entry = tk.Entry(frame)

id_entry.grid(row=0, column=1)
name_entry.grid(row=1, column=1)
rank_entry.grid(row=2, column=1)
salary_entry.grid(row=3, column=1)

btn_frame1 = tk.Frame(root)
btn_frame1.pack(pady=8)

tk.Button(btn_frame1, text="Insert", width=10, command=insert_employee).grid(row=0, column=0, padx=4)
tk.Button(btn_frame1, text="Search", width=10, command=search_employee).grid(row=0, column=1, padx=4)
tk.Button(btn_frame1, text="Clear", width=10, command=clear_fields).grid(row=0, column=2, padx=4)

btn_frame2 = tk.Frame(root)
btn_frame2.pack(pady=8)

tk.Button(btn_frame2, text="In-order", width=12, command=show_inorder).grid(row=0, column=0, padx=4)
tk.Button(btn_frame2, text="Pre-order", width=12, command=show_preorder).grid(row=0, column=1, padx=4)
tk.Button(btn_frame2, text="Post-order", width=12, command=show_postorder).grid(row=0, column=2, padx=4)

tk.Label(root, text="Traversal Output").pack()

output_box = tk.Text(root, height=10, width=60)
output_box.pack(pady=5)

tk.Button(root, text="Exit", width=10, command=root.destroy).pack(pady=10)

root.mainloop()
