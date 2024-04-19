import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Create a database connection
conn = sqlite3.connect('user_accounts.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
conn.commit()


def calculate_grade(entry_grades, entry_weights, tree):
    try:
        grades = [float(grade) for grade in entry_grades.split(",")]
        weights = [float(weight) for weight in entry_weights.split(",")]
    except ValueError:
        messagebox.showerror("Error", "Please enter valid grades and weights separated by commas.")
        return

    if len(grades) != len(weights):
        messagebox.showerror("Error", "Number of grades and weights must match.")
        return

    final_grade = sum(grade * weight for grade, weight in zip(grades, weights))
    messagebox.showinfo("Final Grade", f"Your final grade is: {final_grade:.2f}")

    # Update Treeview with entered grades and weights
    for i, (grade, weight) in enumerate(zip(grades, weights), start=1):
        tree.insert("", "end", values=(f"Assessment {i}", grade, weight, grade * weight))


def calculate_suggestions(entry_grades, weights, desired_grade):
    try:
        grades = [float(grade) for grade in entry_grades.split(",")]
    except ValueError:
        messagebox.showerror("Error", "Please enter valid grades separated by commas.")
        return

    if len(grades) != len(weights):
        messagebox.showerror("Error", "Number of grades and weights must match.")
        return

    current_grade = sum(grade * weight for grade, weight in zip(grades, weights))
    remaining_weight = 1 - sum(weights)
    remaining_points = desired_grade - current_grade
    suggested_grade = remaining_points / remaining_weight
    messagebox.showinfo("Suggestions",
                        f"To achieve a final grade of {desired_grade:.2f}, you need to score an average of {suggested_grade:.2f} on the remaining assessments.")


def create_account(entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        return


def main():
    root = tk.Tk()
    root.title("Grade Tracker")

    lbl_grades = tk.Label(root, text="Enter your grades (separated by commas):")
    lbl_grades.grid(row=0, column=0, padx=10, pady=5)

    entry_grades = tk.Entry(root)
    entry_grades.grid(row=0, column=1, padx=10, pady=5)

    lbl_weights = tk.Label(root, text="Enter the weights (separated by commas):")
    lbl_weights.grid(row=1, column=0, padx=10, pady=5)

    entry_weights = tk.Entry(root)
    entry_weights.grid(row=1, column=1, padx=10, pady=5)

    lbl_desired_grade = tk.Label(root, text="Enter your desired final grade:")
    lbl_desired_grade.grid(row=2, column=0, padx=10, pady=5)

    entry_desired_grade = tk.Entry(root)
    entry_desired_grade.grid(row=2, column=1, padx=10, pady=5)

    lbl_username = tk.Label(root, text="Enter your username:")
    lbl_username.grid(row=3, column=0, padx=10, pady=5)

    entry_username = tk.Entry(root)
    entry_username.grid(row=3, column=1, padx=10, pady=5)

    lbl_password = tk.Label(root, text="Enter your password:")
    lbl_password.grid(row=4, column=0, padx=10, pady=5)

    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=4, column=1, padx=10, pady=5)

    btn_calculate_grade = tk.Button(root, text="Calculate Grade",
                                    command=lambda: calculate_grade(entry_grades.get(), entry_weights.get(), tree))
    btn_calculate_grade.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    btn_calculate_suggestions = tk.Button(root, text="Calculate Suggestions",
                                          command=lambda: calculate_suggestions(entry_grades.get(),
                                                                                [float(weight) for weight in
                                                                                 entry_weights.get().split(",")],
                                                                                float(entry_desired_grade.get())))
    btn_calculate_suggestions.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    btn_create_account = tk.Button(root, text="Create Account",
                                   command=lambda: create_account(entry_username, entry_password))
    btn_create_account.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    # Treeview widget for displaying progress
    tree = ttk.Treeview(root, columns=('Assessment', 'Grade', 'Weight', 'Contribution'))
    tree.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
    tree.heading('#0', text='ID')
    tree.heading('Assessment', text='Assessment')
    tree.heading('Grade', text='Grade')
    tree.heading('Weight', text='Weight')
    tree.heading('Contribution', text='Contribution')

    root.mainloop()


if __name__ == "__main__":
    main()
