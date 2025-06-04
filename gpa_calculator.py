import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import matplotlib.pyplot as plt

# Grade to point mapping
grade_points = {
    "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0,
    "B-": 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "F": 0.0
}

subjects = []

# GPA Calculation Logic
def add_subject(subject_entry, grade_var, credit_entry, subject_list):
    try:
        subject = subject_entry.get()
        grade = grade_var.get()
        credits = float(credit_entry.get())

        if not subject or grade not in grade_points or credits <= 0:
            raise ValueError("Enter valid subject, grade, and credit.")

        subjects.append({"subject": subject, "grade": grade, "credits": credits})
        subject_list.insert(tk.END, f"{subject} | {grade} | {credits} cr")
        subject_entry.delete(0, tk.END)
        credit_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_entries(name_entry, reg_entry, subject_entry, credit_entry, subject_list, gpa_label):
    global subjects
    name_entry.delete(0, tk.END)
    reg_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    credit_entry.delete(0, tk.END)
    subject_list.delete(0, tk.END)
    gpa_label.config(text="GPA: --")
    subjects.clear()


def calculate_gpa(name_entry, reg_entry, gpa_label):
    try:
        name = name_entry.get()
        reg_no = reg_entry.get()
        if not name or not reg_no:
            raise ValueError("Name and Reg No required.")
        if not subjects:
            raise ValueError("Add at least one subject.")

        total_points = sum(grade_points[s["grade"]] * s["credits"] for s in subjects)
        total_credits = sum(s["credits"] for s in subjects)
        gpa = round(total_points / total_credits, 2)

        gpa_label.config(text=f"GPA: {gpa}")

        os.makedirs("gpa_records", exist_ok=True)
        data = {"name": name, "reg_no": reg_no, "gpa": gpa, "subjects": subjects}
        with open(f"gpa_records/{reg_no}.json", "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Saved", f"GPA saved for {name}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# View Records
def load_records(record_list):
    record_list.delete(0, tk.END)
    if not os.path.exists("gpa_records"):
        return
    for file in os.listdir("gpa_records"):
        if file.endswith(".json"):
            record_list.insert(tk.END, file)

def view_selected_record(record_list, record_output):
    try:
        selected = record_list.get(record_list.curselection())
        with open(f"gpa_records/{selected}") as f:
            data = json.load(f)

        display = f"Name: {data['name']}\nReg No: {data['reg_no']}\nGPA: {data['gpa']}\n\nSubjects:\n"
        for s in data["subjects"]:
            display += f" - {s['subject']}: {s['grade']} ({s['credits']} cr)\n"

        record_output.delete(1.0, tk.END)
        record_output.insert(tk.END, display)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def export_record(record_output):
    try:
        content = record_output.get(1.0, tk.END)
        if not content.strip():
            raise ValueError("No record loaded.")
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            with open(file, "w") as f:
                f.write(content)
            messagebox.showinfo("Exported", "Exported to .txt")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GPA Graph
def plot_gpa_graph():
    if not os.path.exists("gpa_records"):
        messagebox.showinfo("No Data", "No records found.")
        return

    names = []
    gpas = []
    for file in os.listdir("gpa_records"):
        with open(f"gpa_records/{file}") as f:
            data = json.load(f)
            names.append(data["name"])
            gpas.append(data["gpa"])

    if not names:
        messagebox.showinfo("No Data", "No data to plot.")
        return

    plt.bar(names, gpas, color='teal')
    plt.xlabel("Student")
    plt.ylabel("GPA")
    plt.title("GPA Comparison")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_help():
    help_win = tk.Toplevel()
    help_win.title("How to Use")
    help_win.geometry("600x500")
    help_win.resizable(False, False)

    instructions = (
        "📌 How to Use the Student Marks Calculator\n\n\n"
        "1.📝 Click 'Add Marks' to enter student name, reg no, and subject details.\n\n"
        "   ➕ Add each subject with grade and credit hours.\n\n"
        "   💾 Click 'Calculate GPA & Save' to store the record.\n\n\n"
        "2.📂 Click 'View Records' to see all saved students.\n\n"
        "   📄 Select a record and view full details.\n\n"
        "   🖨 Export record to .txt if needed.\n\n\n"
        "3.📈 Click 'GPA Graph' to view a comparison of all students' GPA scores.\n\n\n"
        "✅ You can exit anytime using the '❌ Exit' button on the home screen.\n\n\n\n"
        "\n\n \t\t\t- Gayanthaka heshan -"
    )

    tk.Label(help_win, text=instructions, justify="left",padx=20, pady=20, font=("Arial", 11),bg="#aeb8a9").pack()


# GUI Setup
root = tk.Tk()
root.title("🎓 Student Marks Calculator")
root.geometry("620x690")
root.iconbitmap(r'C:\Users\Gayanthaka\Desktop\check\gpa.ico')
root.resizable(False, False)

root.configure(bg="GREY")

frames = {}
def show_frame(name):
    frames[name].tkraise()

# ---------------- Home Page ----------------
home = tk.Frame(root)
home.configure(bg="#aeb8a9")
home.grid(row=0, column=0, sticky="nsew")
frames["home"] = home

tk.Label(home, text="🎓 Student Marks Calculator", font=("Arial", 20, "bold"),fg='blue',bg="#aeb8a9").pack(pady=20)

# Centering buttons in a frame inside 'home'
home_buttons = tk.Frame(home)
home_buttons.pack(expand=True)
home_buttons.configure(bg="#aeb8a9")
tk.Button(home_buttons, text="📝 Add Marks", width=25, height=2, command=lambda: show_frame("add"),bg="#d3d3d3").pack(pady=10)
tk.Button(home_buttons, text="📂 View Records",bg="#d3d3d3", width=25, height=2,
          command=lambda: [load_records(record_list), show_frame("view")]).pack(pady=10)
tk.Button(home_buttons, text="📈 GPA Graph", width=25, height=2, command=lambda: show_frame("graph"),bg="#d3d3d3").pack(pady=10)

tk.Button(home_buttons, text="ℹ️ How to Use", width=25, height=2, command=show_help,bg="#d3d3d3").pack(pady=10)
tk.Button(home_buttons, text="❌ Exit", width=25, height=2, command=root.quit,bg="#d3d3d3").pack(pady=30)


# ---------------- Add Marks Page ----------------
add = tk.Frame(root)
add.grid(row=0, column=0, sticky="nsew")
frames["add"] = add
add.configure(bg="#aeb8a9")
tk.Label(add, text="📝 Add Student Marks", font=("Arial", 16, "bold"),bg="#aeb8a9").pack(pady=10)

name_entry = tk.Entry(add, width=30)
reg_entry = tk.Entry(add, width=30)
subject_entry = tk.Entry(add, width=30)
credit_entry = tk.Entry(add, width=30)
grade_var = tk.StringVar(value="A")

tk.Label(add, text="Student Name:",bg="#aeb8a9").pack()
name_entry.pack()
tk.Label(add, text="Reg No:",bg="#aeb8a9").pack()
reg_entry.pack()
tk.Label(add, text="Subject Name:",bg="#aeb8a9").pack()
subject_entry.pack()
tk.Label(add, text="Grade:",bg="#aeb8a9").pack()
tk.OptionMenu(add, grade_var, *grade_points.keys()).pack()
tk.Label(add, text="Credit Hours:",bg="#aeb8a9").pack()
credit_entry.pack()

subject_list = tk.Listbox(add, width=50)
subject_list.pack(pady=10)

gpa_label = tk.Label(add, text="GPA: --", font=("Arial", 14),bg="#aeb8a9")
gpa_label.pack()

tk.Button(add, text="➕ Add Subject", bg="#2196F3", fg="white",
          command=lambda: add_subject(subject_entry, grade_var, credit_entry, subject_list)).pack(pady=5)

tk.Button(add, text="💾 Calculate GPA & Save", bg="#4CAF50", fg="white",
          command=lambda: calculate_gpa(name_entry, reg_entry, gpa_label)).pack(pady=5)
tk.Button(add, text="🧹 Clear All", bg="#9E9E9E", fg="white",
          command=lambda: clear_entries(name_entry, reg_entry, subject_entry, credit_entry, subject_list, gpa_label)).pack(pady=5)


tk.Button(add, text="⬅ Back", command=lambda: show_frame("home")).pack(pady=10)

# ---------------- View Records Page ----------------
view = tk.Frame(root)
view.grid(row=0, column=0, sticky="nsew")
frames["view"] = view
view.configure(bg="#aeb8a9")

tk.Label(view, text="📂 View Records", font=("Arial", 16, "bold"),bg="#aeb8a9").pack(pady=10)

record_list = tk.Listbox(view, width=50)
record_list.pack(pady=5)

tk.Button(view, text="📄 View Selected", command=lambda: view_selected_record(record_list, record_output),bg="#d3d3d3").pack(pady=5)
record_output = tk.Text(view, width=80, height=20)
record_output.pack(pady=5)

tk.Button(view, text="🖨 Export to TXT", bg="#FF9800", command=lambda: export_record(record_output)).pack(pady=5)
tk.Button(view, text="⬅ Back", command=lambda: show_frame("home")).pack(pady=10)

# ---------------- GPA Graph Page ----------------
graph = tk.Frame(root)
graph.grid(row=0, column=0, sticky="nsew")
frames["graph"] = graph
graph.configure(bg="#aeb8a9")

tk.Label(graph, text="📈 GPA Graph", font=("Arial", 16, "bold"),bg="#aeb8a9").pack(pady=20)
tk.Button(graph, text="📊 Show Graph", command=plot_gpa_graph, bg="#673AB7", fg="white").pack(pady=10)
tk.Button(graph, text="⬅ Back", command=lambda: show_frame("home")).pack(pady=20)

# Start the application
show_frame("home")
root.mainloop()
