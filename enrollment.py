import sqlite3
from sys import excepthook
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("enrollment.db")

# --- TABLE CREATION ---

# 1️⃣ Department Table
conn.execute("""
CREATE TABLE IF NOT EXISTS departments (
dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE)""")

# 2️⃣ Professor Table
conn.execute("""
CREATE TABLE IF NOT EXISTS professors (
prof_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
dept_id INTEGER NOT NULL,
FOREIGN KEY(dept_id) REFERENCES departments(dept_id))""")

# 3️⃣ Student Table
conn.execute("""
CREATE TABLE IF NOT EXISTS students (
student_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
age INTEGER NOT NULL,
dept_id INTEGER,
FOREIGN KEY(dept_id) REFERENCES departments(dept_id))""")

# 4️⃣ Course Table #course id/code
conn.execute("""
CREATE TABLE IF NOT EXISTS courses (
course_code INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
prof_id INTEGER,
dept_id INTEGER,
units INTEGER NOT NULL DEFAULT 3,
schedule text,
FOREIGN KEY(prof_id) REFERENCES professors(prof_id),
FOREIGN KEY(dept_id) REFERENCES departments(dept_id))""")

# 5️⃣ Enrollment Table #enrollment id/no
conn.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
enrollment_no INTEGER PRIMARY KEY AUTOINCREMENT,
student_id INTEGER NOT NULL,
course_code INTEGER NOT NULL,
UNIQUE(student_id, course_code),
FOREIGN KEY(student_id) REFERENCES students(student_id),
FOREIGN KEY(course_code) REFERENCES courses(course_code))""")

conn.commit()

# --- CLASSES ---
class Department:
    def __init__(self, name, dept_id=None):
        self.dept_id = dept_id
        self.name = name

    #CREATE
    @staticmethod #<---just preference for consistency of how i call my func
    def add_dept(name):
        with conn:
            conn.execute("INSERT INTO departments (name) VALUES (?)", (name,))
        print(f"Department of {name} added!")

    def add_depts(dept_list):
        #dept_list = ["CS", "Math", "Physics"]
        with conn:
            conn.executemany("INSERT INTO departments (name) VALUES (?)",[(name,) for name in dept_list])
        print(f"Departments of {dept_list} added!")

    # READ
    def get_dept(dept_id):
        try:
            query = "SELECT * FROM departments WHERE dept_id = ?"
            df = pd.read_sql_query(query, conn, params=(dept_id, )) #turning query to df

            if df.empty:
                print(f"No department found for dept_id={dept_id}")
                return None

            # Convert DataFrame to dict (records format gives a list of dicts)
            dept_dict = df.to_dict(orient='records')[0]  # Get the first record
            print(dept_dict)
            return dept_dict

        except Exception as e:
            print("Database error:", e)
            return None

    def get_depts(self):
        try:
            query = "SELECT * FROM departments"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                print("No departments found.")
                return []

            dept_list = df.to_dict(orient='records')  # List of dictionaries
            print(dept_list)
            return dept_list

        except Exception as e:
            print("Database error:", e)
            return []

    # UPDATE
    def update_dept(dept_id, name):
        with conn:
            conn.execute("UPDATE departments SET name=? WHERE dept_id=?", (name, dept_id))
        print("update complete")

    def update_depts(dept_list):
        # dept_list = [(new_name, dept_id)]
        with conn:
            conn.executemany("UPDATE departments SET name = ? WHERE dept_id = ?", dept_list)
        print("update complete")

    # DELETE
    def del_dept(dept_id):
        with conn:
            conn.execute("DELETE FROM departments WHERE dept_id=?", (dept_id,))
        print("deletion complete")


    def del_depts(dept_ids):
        #del_depts([1, 3, 5])
        with conn:
            conn.executemany("DELETE FROM departments WHERE dept_id = ?",
                         [(dept_id,) for dept_id in dept_ids])
        print("deletion complete")

class Professor:
    def __init__(self,name, dept_id, prof_id=None):
        self.prof_id = prof_id
        self.name = name
        self.dept_id = dept_id

    # CREATE
    @staticmethod
    def add_prof(name, dept_id):
        with conn:
            conn.execute("INSERT INTO professors (name, dept_id) VALUES (?, ?)",
                     (name, dept_id))
        print(f"Professor {name} added!")

    def add_profs(prof_list):
        # prof_list = [(name, dept_id), (name, dept_id)]
        with conn:
            conn.executemany("INSERT INTO professors (name, dept_id) VALUES (?, ?)",prof_list)
        print(f"Professors: {prof_list} added!")

    # READ
    def get_prof(prof_id):
        try:
            query = "SELECT * FROM professors WHERE prof_id = ?"
            df = pd.read_sql_query(query, conn, params=(prof_id,))

            if df.empty:
                print(f"No professor found for prof_id={prof_id}")
                return None

            prof_dict = df.to_dict(orient='records')[0]
            print(prof_dict)
            return prof_dict

        except Exception as e:
            print("Database error:", e)
            return None

    def get_profs(self):
        try:
            query = "SELECT * FROM professors"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                print("No professors found.")
                return []

            prof_list = df.to_dict(orient='records')
            print(prof_list)
            return prof_list

        except Exception as e:
            print("Database error:", e)
            return []

    # UPDATE
    def update_prof(prof_id, name):
        with conn:
            conn.execute("UPDATE professors SET name=? WHERE prof_id=?", (name, prof_id))
        print("update complete")

    def update_profs(prof_list):
        # prof_list = [(new_name, prof_id)]
        with conn:
            conn.executemany("UPDATE professors SET name = ? WHERE prof_id = ?", prof_list)
        print("update complete")

    # DELETE
    def del_prof(prof_id):
        with conn:
            conn.execute("DELETE FROM professors WHERE prof_id=?",(prof_id,))
        print("deletion complete")

    def del_profs(prof_ids):
        # prof_ids = [1, 2, 3]
        with conn:
            conn.executemany(
                "DELETE FROM professors WHERE prof_id = ?",
                [(prof_id,) for prof_id in prof_ids]
            )
        print("deletion complete")

class Student:
    def __init__(self, name, age, dept_id, student_id=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.dept_id = dept_id

    # CREATE
    @staticmethod
    def add_student(name, age, dept_id):
        with conn:
            conn.execute("INSERT INTO students (name, age, dept_id) VALUES (?, ?, ?)",
                     (name, age, dept_id))
        print(f"Student {name} added!")

    def add_students(students_list):
        # students_list = [(name, age, dept_id)]
        with conn:
            conn.executemany("INSERT INTO students (name, age, dept_id) VALUES (?, ?, ?)",students_list)
        print(f"Students: {students_list} added!")

    # READ
    def get_student(student_id):
        try:
            query = "SELECT * FROM students WHERE student_id = ?"
            df = pd.read_sql_query(query, conn, params=(student_id,))

            if df.empty:
                print(f"No student found for student_id={student_id}")
                return None

            student_dict = df.to_dict(orient='records')[0]  # first row as dict
            print(student_dict)
            return student_dict

        except Exception as e:
            print("Database error:", e)
            return None

    def get_students(self):
        try:
            query = "SELECT * FROM students"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                print("No students found.")
                return []

            students = df.to_dict(orient='records')
            print(students)
            return students

        except Exception as e:
            print("Database error:", e)
            return []

    # UPDATE
    def update_student(student_id, name, age):
        with conn:
            conn.execute("UPDATE students SET name=?, age=? WHERE student_id=?",
                         (name, age, student_id))
        print("update complete")

    def update_students(students_list):
        # students_list = [(new_name, students_id)]
        with conn:
            conn.executemany("UPDATE students SET name = ?, age=? WHERE student_id = ?", students_list)
        print("update complete")

    # DELETE
    def del_student(student_id):
        with conn:
            conn.execute("DELETE FROM students WHERE student_id=?",(student_id,))
        print("deletion complete")

    def del_students(student_ids):
        #del_students([1, 3, 5])
        with conn:
            conn.executemany("DELETE FROM students WHERE student_id = ?",
                         [(student_id,) for student_id in student_ids])
        print("deletion complete")

class Course:
    total_units = 0
    def __init__(self, name, prof_id, dept_id, units, schedule, course_code=None):
        self.course_code = course_code
        self.name = name
        self.prof_id = prof_id
        self.dept_id = dept_id
        self.schedule=schedule
        self.units = units

    # CREATE
    @staticmethod
    def add_course(name, prof_id, dept_id, units, schedule):
        with conn: #<---for transaction rollback, omits error and auto commits on success unlike conn.commit
            conn.execute("""INSERT INTO courses (name, prof_id, dept_id, units, schedule)
                     VALUES (?, ?, ?, ?, ?)"""
                    ,(name, prof_id, dept_id, units, schedule))
        print(f"Course {name} added!")

    def add_courses(courses_list):
        # courses_list = [(name, prof_id, dept_id, units, schedule)]
        with conn:
            conn.executemany( """INSERT INTO courses (name, prof_id, dept_id, units, schedule)
               VALUES (?, ?, ?, ?, ?)""", courses_list)
        print(f"Courses: {courses_list} added!")

    # READ
    def get_course(course_code):
        try:
            query = "SELECT * FROM courses WHERE course_code = ?"
            df = pd.read_sql_query(query, conn, params=(course_code,))

            if df.empty:
                print(f"No course found for course_code={course_code}")
                return None

            course_dict = df.to_dict(orient='records')[0]
            print(course_dict)
            return course_dict

        except Exception as e:
            print("Database error:", e)
            return None

    def get_courses(self):
        try:
            query = "SELECT * FROM courses"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                print("No courses found.")
                return []

            courses = df.to_dict(orient='records')
            print(courses)
            return courses

        except Exception as e:
            print("Database error:", e)
            return []

    # UPDATE
    def update_course(course_code, name, units, schedule):
        with conn:
            conn.execute("UPDATE courses SET name=?, units=?, schedule=? WHERE course_code=?",
                         (name, units, schedule,course_code))
        print("update complete")

    def update_courses(courses_list):
        # courses_list = [(new_name, new_units, schedule, course_code)]
        with conn:
            conn.executemany("UPDATE courses SET name = ?, units = ?, schedule=? WHERE course_code = ?",
            courses_list)

    # DELETE
    def del_course(course_code):
        with conn:
            conn.execute("DELETE FROM courses WHERE course_code=?",(course_code,))
        print("deletion complete")

    def del_courses(course_codes):
        #del_courses([1, 3, 5])
        with conn:
            conn.executemany("DELETE FROM courses WHERE course_code = ?",
                         [(course_code,) for course_code in course_codes])
        print("deletion complete")

class Enrollment:
    def __init__(self, student_id, course_code, enrollment_no=None):
        self.enrollment_no = enrollment_no
        self.student_id = student_id
        self.course_code = course_code

    # CREATE
    @staticmethod
    def add_enrollment(student_id, course_code):
        #Check total enrolled units for this student ---
        cursor = conn.execute("""
            SELECT IFNULL(SUM(c.units), 0)
            FROM enrollments e
            JOIN courses c ON e.course_code = c.course_code
            WHERE e.student_id = ?
        """, (student_id,))
        current_units = cursor.fetchone()[0]

        cursor = conn.execute("""
            SELECT units FROM courses WHERE course_code = ?
        """, (course_code,))
        new_course_units = cursor.fetchone()[0]

        if current_units + new_course_units > 18:
            print(f"Enrollment denied: total would be {current_units + new_course_units} units (limit is 18).")
            return

        try:
            with conn:
                conn.execute("""
                       INSERT INTO enrollments (student_id, course_code)
                       VALUES (?, ?)
                   """, (student_id, course_code))
            print("Enrollment successful")
        except sqlite3.IntegrityError as e:
            print(f"Enrollment failed: {e}")

    def add_enrollments(enrollments_list):
        # Check total enrolled units for this student
        with conn:
            for student_id, course_code in enrollments_list:
                # Check total enrolled units
                cursor = conn.execute("""
                    SELECT IFNULL(SUM(c.units), 0)
                    FROM enrollments e
                    JOIN courses c ON e.course_code = c.course_code
                    WHERE e.student_id = ?
                """, (student_id,))
                current_units = cursor.fetchone()[0]

                cursor = conn.execute("SELECT units FROM courses WHERE course_code = ?", (course_code,))
                new_units = cursor.fetchone()[0]

                if current_units + new_units > 18:
                    print(f"Enrollment denied for student {student_id}: total would be {current_units + new_units} units.")
                    continue  # Skip this enrollment

                conn.execute("INSERT INTO enrollments (student_id, course_code) VALUES (?, ?)",
                    (student_id, course_code))
                print("Enrollment successful")

    # READ
    def get_enrollment(enrollment_no):
        try:
            query = "SELECT * FROM enrollments WHERE enrollment_no = ?"
            df = pd.read_sql_query(query, conn, params=(enrollment_no,))

            if df.empty:
                print(f"No enrollment found for enrollment_no={enrollment_no}")
                return None

            enrollment_dict = df.to_dict(orient='records')[0]
            print(enrollment_dict)
            return enrollment_dict

        except Exception as e:
            print("Database error:", e)
            return None

    def get_enrollments(self):
        try:
            query = "SELECT * FROM enrollments"
            df = pd.read_sql_query(query, conn)

            if df.empty:
                print("No enrollments found.")
                return []

            enrollments = df.to_dict(orient='records')
            print(enrollments)
            return enrollments

        except Exception as e:
            print("Database error:", e)
            return []

    # UPDATE
    #Enrollment contains only primary keys and foreign keys, updating it directly is a bad idea

    # DELETE
    def del_enrollment(enrollment_no):
        with conn:
            conn.execute("DELETE FROM enrollments WHERE enrollment_number=?",(enrollment_no,))
        print("deletion complete")

    def del_enrollments(enrollment_nos):
        #del_enrollments([1, 3, 5])
        with conn:
            conn.executemany("DELETE FROM enrollments WHERE enrollment_no = ?",
                         [(enrollment_no,) for enrollment_no in enrollment_nos])
        print("deletion complete")

#REPORTS & ANALYTICS

def course_roster():
    """ Course roster with professor name and enrolled student list"""
    query = """
    SELECT 
        c.course_code,
        c.name AS course_name,
        p.name AS professor_name,
        s.name AS student_name
    FROM courses c
    JOIN professors p ON c.prof_id = p.prof_id
    LEFT JOIN enrollments e ON c.course_code = e.course_code
    LEFT JOIN students s ON e.student_id = s.student_id
    ORDER BY c.course_code, s.name;
    """
    df = pd.read_sql_query(query, conn)
    print("COURSE ROSTER")
    if df.empty:
        print("No enrollments found.")
    else:
        print(df)
    return df

def student_timetable(student_id):
    """Individual student’s timetable"""
    query = """
    SELECT 
        s.name AS student_name,
        c.name AS course_name,
        c.units,
        c.schedule,  -- 🆕 show the schedule
        p.name AS professor_name,
        d.name AS department_name
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_code = c.course_code
    JOIN professors p ON c.prof_id = p.prof_id
    JOIN departments d ON c.dept_id = d.dept_id
    WHERE s.student_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(student_id,))
    print(f"TIMETABLE FOR STUDENT {student_id}")
    if df.empty:
        print("No courses enrolled.")
    else:
        print(df)
        print(f"Total Units: {df['units'].sum()}")
    return df

def department_summary():
    """Department-level summary (#courses, #students, average section size)"""
    query = """
    SELECT 
        d.name AS department,
        COUNT(DISTINCT c.course_code) AS num_courses,
        COUNT(DISTINCT s.student_id) AS num_students,
        ROUND(AVG(enrollment_count), 2) AS avg_section_size
    FROM departments d
    LEFT JOIN courses c ON d.dept_id = c.dept_id
    LEFT JOIN professors p ON c.prof_id = p.prof_id
    LEFT JOIN enrollments e ON c.course_code = e.course_code
    LEFT JOIN students s ON e.student_id = s.student_id
    LEFT JOIN (
        SELECT course_code, COUNT(*) AS enrollment_count
        FROM enrollments
        GROUP BY course_code
    ) ec ON c.course_code = ec.course_code
    GROUP BY d.name;
    """
    df = pd.read_sql_query(query, conn)
    print("DEPARTMENT SUMMARY")
    if df.empty:
        print("No data found.")
    else:
        print(df)
    return df

def plot_enrollment_by_department():
    """Optional pandas visualization: total enrollments per department"""
    query = """
    SELECT 
        d.name AS department,
        COUNT(e.enrollment_no) AS total_enrollments
    FROM departments d
    LEFT JOIN courses c ON d.dept_id = c.dept_id
    LEFT JOIN enrollments e ON c.course_code = e.course_code
    GROUP BY d.name;
    """
    df = pd.read_sql_query(query, conn)
    df.plot(kind='bar', x='department', y='total_enrollments', title='Enrollments per Department')
    plt.show()
    return df


def analyze_enrollment_by_department():
    """Exports enrollments per department into a DataFrame and visualizes results."""

    # --- Step 1: Query the database into a pandas DataFrame ---
    query = """
    SELECT 
        d.name AS department,
        COUNT(e.enrollment_no) AS total_enrollments
    FROM departments d
    LEFT JOIN courses c ON d.dept_id = c.dept_id
    LEFT JOIN enrollments e ON c.course_code = e.course_code
    GROUP BY d.name
    ORDER BY total_enrollments DESC;
    """

    df = pd.read_sql_query(query, conn)

    # --- Step 2: Display DataFrame content ---
    print("ENROLLMENTS PER DEPARTMENT")
    print(df)

    # --- Step 3: Simple descriptive analysis ---
    total = df["total_enrollments"].sum()
    avg = df["total_enrollments"].mean()
    most = df.loc[df["total_enrollments"].idxmax(), "department"] if not df.empty else None

    print("ANALYSIS SUMMARY")
    print(f"Total Enrollments: {total}")
    print(f"Average Enrollments per Department: {avg:.2f}")
    print(f"Department with Most Enrollments: {most}")

    # --- Step 4: Visualization ---
    df.plot(kind='bar', x='department', y='total_enrollments',
            title='Enrollments per Department', legend=False, figsize=(7, 4))
    plt.show()
    return df

#TESTING

Student.del_student(8)
#readding student chnages in number due to autoincrement
Student.add_student("Heidi Clark", 19, 2)

Student.get_students(0)