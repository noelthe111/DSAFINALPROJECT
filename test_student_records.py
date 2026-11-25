# Simple tests for the Student Record Management System.
# Run with:  python test_student_records.py

import student_records as sr


def reset():
    """Empty the list before each test."""
    sr.students.clear()


def load_sample():
    sr.add_student(103, "Carla Reyes", 3.2)
    sr.add_student(101, "Ben Santos", 3.9)
    sr.add_student(102, "Ana Cruz", 3.2)
    sr.add_student(104, "Ana Cruz", 2.5)  # duplicate name on purpose


def ids(records):
    return [s["id"] for s in records]


def test_add_and_duplicate_id():
    reset()
    ok, _ = sr.add_student(1, "Ana", 3.0)
    assert ok is True
    ok, _ = sr.add_student(1, "Someone Else", 2.0)
    assert ok is False
    assert len(sr.students) == 1


def test_view_by_id():
    reset()
    load_sample()
    assert sr.get_student(101)["name"] == "Ben Santos"
    assert sr.get_student(999) is None


def test_update_name_gpa_and_id():
    reset()
    load_sample()
    assert sr.update_student(101, None, "Benjamin Santos", None)[0] is True
    assert sr.get_student(101)["name"] == "Benjamin Santos"
    assert sr.update_student(101, None, None, 3.5)[0] is True
    assert sr.get_student(101)["gpa"] == 3.5
    assert sr.update_student(101, 200, None, None)[0] is True
    assert sr.get_student(200) is not None and sr.get_student(101) is None


def test_update_prevents_duplicate_id():
    reset()
    load_sample()
    ok, _ = sr.update_student(101, 102, None, None)
    assert ok is False
    assert sr.get_student(101) is not None  # unchanged


def test_update_missing_student():
    reset()
    assert sr.update_student(5, None, "X", None)[0] is False


def test_remove():
    reset()
    load_sample()
    assert sr.remove_student(101)[0] is True
    assert sr.get_student(101) is None
    assert sr.remove_student(101)[0] is False  # already gone


def test_list_by_id():
    reset()
    load_sample()
    assert ids(sr.list_by_id()) == [101, 102, 103, 104]


def test_sort_by_gpa_highest_first_ties_by_id():
    reset()
    load_sample()
    # 3.9 (101), then 3.2 tie -> 102, 103, then 2.5 (104)
    assert ids(sr.sort_by_gpa()) == [101, 102, 103, 104]


def test_sort_by_name_ties_by_id():
    reset()
    load_sample()
    # Ana Cruz (102), Ana Cruz (104), Ben Santos (101), Carla Reyes (103)
    assert ids(sr.sort_by_name()) == [102, 104, 101, 103]


def test_find_by_name_shows_all_matches():
    reset()
    load_sample()
    assert ids(sr.find_by_name("ana cruz")) == [102, 104]  # not case-sensitive
    assert len(sr.find_by_name("Nobody")) == 0


def test_validation():
    assert sr.is_valid_id("12") is True
    assert sr.is_valid_id("0") is False
    assert sr.is_valid_id("-3") is False
    assert sr.is_valid_id("abc") is False
    assert sr.is_valid_name("Ana") is True
    assert sr.is_valid_name("   ") is False
    assert sr.is_valid_name("R2D2") is False
    assert sr.is_valid_gpa("3.5") is True
    assert sr.is_valid_gpa("4.5") is False
    assert sr.is_valid_gpa("-1") is False
    assert sr.is_valid_gpa("abc") is False


# Run every function whose name starts with "test_"
all_tests = [name for name in dir() if name.startswith("test_")]
for name in all_tests:
    globals()[name]()
    print("PASS:", name)
print("\nAll " + str(len(all_tests)) + " tests passed.")
