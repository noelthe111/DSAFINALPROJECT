# Student Record Management System
# Simple beginner-style program: records are kept in a list of dictionaries.
# Each record looks like: {"id": "S101", "name": "Ana Cruz", "gpa": 3.5}

students = []  # the "database" (kept in memory only)


# ---------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------

def find_index_by_id(student_id):
    """Return the position of a student in the list, or -1 if not found.
    IDs are compared in UPPERCASE, so "s101" and "S101" are the same ID."""
    student_id = student_id.upper()
    for i in range(len(students)):
        if students[i]["id"] == student_id:
            return i
    return -1


def is_valid_id(text):
    """An ID must not be empty, and may only contain letters, digits, and dashes
    (not even spaceeees). Examples: S101, 2024-001"""
    if text == "":
        return False
    for ch in text:
        if not (ch.isalpha() or ch.isdigit() or ch == "-"):
            return False
    return True


def is_valid_name(text):
    """A name must not be empty and must not contain digits..."""
    if text.strip() == "":
        return False
    for ch in text:
        if ch.isdigit():
            return False
    return True


def is_valid_gpa(text):
    """A GPA must be a number ONLY from 0.0 to 4.0"""
    try:
        value = float(text)
    except ValueError:
        return False
    return 0.0 <= value <= 4.0


def get_sort_value(student, sort_by):
    """Return the value we should compare for one student.
    sort_by is the word "id", "gpa", or "name"."""
    if sort_by == "id":
        return student["id"]
    elif sort_by == "gpa":
        return -student["gpa"]  # negative so the highest GPA comes first
    else:
        return student["name"].lower()  # lowercase so "trexie" and "Trexie" match


def insertion_sort(records, sort_by):
    """Sort a COPY of the list using insertion sort (simple and stable).
    sort_by is the word "id", "gpa", or "name"."""
    result = records[:]
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and get_sort_value(result[j], sort_by) > get_sort_value(current, sort_by):
            result[j + 1] = result[j]
            j = j - 1
        result[j + 1] = current
    return result


# ---------------------------------------------------------------
# Core operations (no input/print here, so they are easy to test)
# ---------------------------------------------------------------

def add_student(student_id, name, gpa):
    """Add a student. Returns (True/False, message)."""
    if find_index_by_id(student_id) != -1:
        return False, "ID " + str(student_id) + " is already in use."
    students.append({"id": student_id.upper(), "name": name.strip(), "gpa": gpa})
    return True, "Student added successfully."


def get_student(student_id):
    """Return the student record, or None if not found."""
    index = find_index_by_id(student_id)
    if index == -1:
        return None
    return students[index]


def update_student(old_id, new_id, new_name, new_gpa):
    """Update a student. Pass None for any value that should stay the same."""
    index = find_index_by_id(old_id)
    if index == -1:
        return False, "No student found with ID " + str(old_id) + "."
    if new_id is not None and new_id.upper() != old_id.upper():
        if find_index_by_id(new_id) != -1:
            return False, "ID " + str(new_id) + " is already in use. No changes made."
        students[index]["id"] = new_id.upper()
    if new_name is not None:
        students[index]["name"] = new_name.strip()
    if new_gpa is not None:
        students[index]["gpa"] = new_gpa
    return True, "Student updated successfully."


def remove_student(student_id):
    """Remove a student by ID."""
    index = find_index_by_id(student_id)
    if index == -1:
        return False, "No student found with ID " + str(student_id) + "."
    students.pop(index)
    return True, "Student removed successfully."


def list_by_id():
    """All students, smallest ID first."""
    return insertion_sort(students, "id")


def sort_by_gpa():
    """All students, highest GPA first. Equal GPAs are ordered by ID."""
    by_id = list_by_id()  # start in ID order so ties stay in ID order
    return insertion_sort(by_id, "gpa")


def sort_by_name():
    """All students, A to Z (ignoring upper/lower case). Equal names are ordered by ID."""
    by_id = list_by_id()
    return insertion_sort(by_id, "name")


def find_by_name(name):
    """Return every student whose name matches (ignoring upper/lower case)."""
    matches = []
    for s in list_by_id():
        if s["name"].lower() == name.strip().lower():
            matches.append(s)
    return matches


# ---------------------------------------------------------------
# User interface
# ---------------------------------------------------------------

def show_students(records):
    """Print a list of students as a small table."""
    if len(records) == 0:
        print("No student records to show.")
        return
    print("-" * 46)
    print("ID".ljust(12) + "Name".ljust(22) + "GPA")
    print("-" * 46)
    for s in records:
        print(s["id"].ljust(12) + s["name"].ljust(22) + format(s["gpa"], ".2f"))
    print("-" * 46)


def ask_id(prompt):
    """Keep asking until the user types a valid ID."""
    while True:
        text = input(prompt).strip()
        if is_valid_id(text):
            return text.upper()
        print("Error: the ID can only have letters, numbers, and dashes (no spaces).")


def ask_name(prompt):
    while True:
        text = input(prompt).strip()
        if is_valid_name(text):
            return text
        print("Error: the name cannot be empty or contain numbers.")


def ask_gpa(prompt):
    while True:
        text = input(prompt).strip()
        if is_valid_gpa(text):
            return float(text)
        print("Error: the GPA must be a number between 0.0 and 4.0.")


def ui_add():
    student_id = ask_id("Enter student ID: ")
    if find_index_by_id(student_id) != -1:  # check early so we don't waste the user's time
        print("Error: ID " + str(student_id) + " is already in use.")
        return
    name = ask_name("Enter name: ")
    gpa = ask_gpa("Enter GPA (0.0 - 4.0): ")
    ok, message = add_student(student_id, name, gpa)
    print(message)


def ui_view():
    student_id = ask_id("Enter student ID to view: ")
    student = get_student(student_id)
    if student is None:
        print("Not found: no student has ID " + str(student_id) + ".")
    else:
        show_students([student])


def ui_update():
    old_id = ask_id("Enter the ID of the student to update: ")
    student = get_student(old_id)
    if student is None:
        print("Not found: no student has ID " + str(old_id) + ".")
        return
    show_students([student])
    print("What would you like to change?")
    print("  1. Name")
    print("  2. GPA")
    print("  3. ID")
    choice = input("Choose 1-3: ").strip()
    if choice == "1":
        ok, message = update_student(old_id, None, ask_name("New name: "), None)
    elif choice == "2":
        ok, message = update_student(old_id, None, None, ask_gpa("New GPA (0.0 - 4.0): "))
    elif choice == "3":
        ok, message = update_student(old_id, ask_id("New ID: "), None, None)
    else:
        print("Error: please choose 1, 2 or 3.")
        return
    print(message)


def ui_remove():
    student_id = ask_id("Enter the ID of the student to remove: ")
    student = get_student(student_id)
    if student is None:
        print("Not found: no student has ID " + str(student_id) + ".")
        return
    show_students([student])
    answer = input("Are you sure you want to remove this student? (y/n): ").strip().lower()
    if answer == "y":
        ok, message = remove_student(student_id)
        print(message)
    else:
        print("Removal cancelled.")


def ui_find_by_name():
    name = ask_name("Enter the name to search for: ")
    matches = find_by_name(name)
    if len(matches) == 0:
        print("Not found: no student is named '" + name + "'.")
    else:
        print(str(len(matches)) + " match(es) found:")
        show_students(matches)


def show_menu():
    print()
    print("===== Student Record Management System =====")
    print("1. Add a student")
    print("2. View a student by ID")
    print("3. Update a student")
    print("4. Remove a student")
    print("5. List all students by ID")
    print("6. Sort by GPA (highest first)")
    print("7. Sort by name (A to Z)")
    print("8. Find student(s) by name")
    print("9. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-9): ").strip()
        print()
        if choice == "1":
            ui_add()
        elif choice == "2":
            ui_view()
        elif choice == "3":
            ui_update()
        elif choice == "4":
            ui_remove()
        elif choice == "5":
            print("All students, ordered by ID (A to Z, then 0 to 9 as text):")
            show_students(list_by_id())
        elif choice == "6":
            print("All students, ordered by GPA (highest first; ties ordered by ID):")
            show_students(sort_by_gpa())
        elif choice == "7":
            print("All students, ordered by name (A to Z; ties ordered by ID):")
            show_students(sort_by_name())
        elif choice == "8":
            ui_find_by_name()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Error: please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()