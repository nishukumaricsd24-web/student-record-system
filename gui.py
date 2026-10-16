# gui.py - Blue-White Dashboard | Only GUI is changed, Backend preserved
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re
import math
import database
from student import Student

# ---------- Theme ----------
BLUE_DARK = "#1A3A5D"
BLUE_PRIMARY = "#2563EB"
BLUE_LIGHT = "#EFF6FF"
BG = "#F1F5F9"
CARD_BG = "#FFFFFF"

COURSES = ["Diploma in Computer Science", "BCA", "B.Tech", "BBA", "MCA"]
COURSE_SECTIONS = {
    "Diploma in Computer Science": ["A", "B", "C"],
    "BCA": ["A", "B", "C"],
    "B.Tech": ["A", "B", "C", "D"],
    "BBA": ["A", "B"],
    "MCA": ["A", "B"]
}

DB_NAME = "students.db"

def ensure_schema():
    """Auto-migrate without touching database.py - preserves data"""
    try:
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        if not cur.fetchone():
            return
        cur.execute("PRAGMA table_info(students)")
        cols = [c[1] for c in cur.fetchall()]
        if "section" not in cols: cur.execute("ALTER TABLE students ADD COLUMN section TEXT")
        if "phone" not in cols: cur.execute("ALTER TABLE students ADD COLUMN phone TEXT")
        if "email" not in cols: cur.execute("ALTER TABLE students ADD COLUMN email TEXT")
        con.commit()
        con.close()
    except: pass

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System")
        self.root.geometry("1240x720")
        self.root.minsize(1100, 650)
        self.root.configure(bg=BG)
        ensure_schema()
        try: database.create_table()
        except: pass
        self.current_course = None
        self.setup_style()
        self.build_ui()
        # Initial Screen: ONLY Add Student
        self.show_screen("add")

    def setup_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=BLUE_DARK, foreground="white")
        s.map("Treeview", background=[("selected", BLUE_LIGHT)])

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BLUE_DARK, height=58)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="  🎓  Student Record Management System", bg=BLUE_DARK, fg="white", font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(header, text="Blue-White Dashboard", bg=BLUE_DARK, fg="#93C5FD", font=("Segoe UI", 9)).pack(side="right", padx=20)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg=BLUE_DARK, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="NAVIGATION", bg=BLUE_DARK, fg="#93C5FD", font=("Segoe UI", 8, "bold")).pack(pady=(18,8))

        def nav(text, key):
            return tk.Button(sidebar, text=text, bg=BLUE_DARK, fg="white", activebackground=BLUE_PRIMARY,
                             activeforeground="white", bd=0, anchor="w", padx=22, pady=12, font=("Segoe UI", 10),
                             cursor="hand2", command=lambda: self.show_screen(key))

        nav("➕  Add Student", "add").pack(fill="x")
        nav("📋  View Students", "view").pack(fill="x")
        nav("🔍  Search Student", "search").pack(fill="x")
        nav("🗂️  Student Records", "records").pack(fill="x")

        # Main Content Area - screens will be swapped here
        self.main = tk.Frame(body, bg=BG)
        self.main.pack(side="right", fill="both", expand=True, padx=16, pady=16)

        self.frames = {}
        self.create_add_screen()
        self.create_view_screen()
        self.create_search_screen()
        self.create_records_screen()

    # ---------- Screen Switching ----------
    def show_screen(self, name):
        for f in self.frames.values(): f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        if name == "view": self.refresh_view_table()
        if name == "records": self.show_course_cards()

    # ---------- 1. ADD STUDENT SCREEN ----------
    def create_add_screen(self):
        f = tk.Frame(self.main, bg=BG)
        self.frames["add"] = f

        title = tk.LabelFrame(f, text="  Student Registration  ", bg=CARD_BG, fg=BLUE_DARK, font=("Segoe UI", 11, "bold"), padx=18, pady=16)
        title.pack(fill="x")

        # Step 1 - Course
        tk.Label(title, text="Select Course *", bg=CARD_BG, fg=BLUE_DARK, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=6)
        self.cmb_course = ttk.Combobox(title, values=COURSES, state="readonly", font=("Segoe UI", 10))
        self.cmb_course.grid(row=1, column=0, sticky="ew", padx=6, pady=(2,12))
        self.cmb_course.set("Select Course")
        self.cmb_course.bind("<<ComboboxSelected>>", self.on_course_change)

        # Step 2 - Section
        tk.Label(title, text="Select Section *", bg=CARD_BG, fg=BLUE_DARK, font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w", padx=6)
        self.cmb_section = ttk.Combobox(title, values=[], state="disabled", font=("Segoe UI", 10))
        self.cmb_section.grid(row=1, column=1, sticky="ew", padx=6, pady=(2,12))
        self.cmb_section.set("Select Section - select course first")

        tk.Label(title, text="Student Details", bg=CARD_BG, fg=BLUE_DARK, font=("Segoe UI", 9, "bold")).grid(row=2, column=0, columnspan=2, sticky="w", padx=6, pady=(4,6))

        tk.Label(title, text="Student Name *", bg=CARD_BG).grid(row=3, column=0, sticky="w", padx=6)
        tk.Label(title, text="Roll Number *", bg=CARD_BG).grid(row=3, column=1, sticky="w", padx=6)
        self.ent_name = ttk.Entry(title, font=("Segoe UI", 10))
        self.ent_roll = ttk.Entry(title, font=("Segoe UI", 10))
        self.ent_name.grid(row=4, column=0, sticky="ew", padx=6, pady=2)
        self.ent_roll.grid(row=4, column=1, sticky="ew", padx=6, pady=2)

        tk.Label(title, text="Phone Number * (10 digits)", bg=CARD_BG).grid(row=5, column=0, sticky="w", padx=6, pady=(8,0))
        tk.Label(title, text="Marks * (0-100)", bg=CARD_BG).grid(row=5, column=1, sticky="w", padx=6, pady=(8,0))
        self.ent_phone = ttk.Entry(title, font=("Segoe UI", 10))
        self.ent_marks = ttk.Entry(title, font=("Segoe UI", 10))
        self.ent_phone.grid(row=6, column=0, sticky="ew", padx=6, pady=2)
        self.ent_marks.grid(row=6, column=1, sticky="ew", padx=6, pady=2)

        title.columnconfigure(0, weight=1)
        title.columnconfigure(1, weight=1)

        tk.Button(title, text="Add Student", bg=BLUE_PRIMARY, fg="white", bd=0, padx=26, pady=9, font=("Segoe UI", 10, "bold"), cursor="hand2", command=self.add_student).grid(row=7, column=0, columnspan=2, pady=(16,4))
        tk.Button(title, text="Clear Form", bg="#64748B", fg="white", bd=0, padx=18, pady=6, cursor="hand2", command=self.clear_add_form).grid(row=8, column=0, columnspan=2)

    def on_course_change(self, e=None):
        course = self.cmb_course.get()
        secs = COURSE_SECTIONS.get(course, ["A","B","C"])
        self.cmb_section.config(values=secs, state="readonly")
        self.cmb_section.set("Select Section")

    def validate_add(self):
        c = self.cmb_course.get(); s = self.cmb_section.get()
        name = self.ent_name.get().strip(); roll = self.ent_roll.get().strip()
        phone = self.ent_phone.get().strip(); marks_s = self.ent_marks.get().strip()
        if c not in COURSES: return False, "Please select Course"
        if s not in COURSE_SECTIONS.get(c, []): return False, "Please select Section (select course first)"
        if not name: return False, "Student Name cannot be empty"
        if not roll:
            return False, "Roll Number cannot be empty"
        try:
            r=int(roll); 
            if r<=0: return False, "Roll Number must be positive"
        except: return False, "Roll Number must be numeric"
        if not re.fullmatch(r"\d{10}", phone): return False, "Phone must be exactly 10 digits"
        if not marks_s: return False, "Marks cannot be empty"
        try:
            m=float(marks_s)
            if not math.isfinite(m) or m<0 or m>100: return False, "Marks must be between 0 and 100"
        except: return False, "Marks must be numeric"
        return True, ""

    def add_student(self):
        ok, msg = self.validate_add()
        if not ok: messagebox.showerror("Validation Error", msg); return
        roll = int(self.ent_roll.get().strip())
        name = self.ent_name.get().strip()
        course = self.cmb_course.get()
        section = self.cmb_section.get()
        phone = self.ent_phone.get().strip()
        marks = float(self.ent_marks.get().strip())
        # Try backend function first, fallback to direct SQL for old database.py
        try:
            # New Student signature supports section/phone
            stu = Student(roll, name, course, marks)
            # attach extra attrs if Student class older
            stu.section = section; stu.phone = phone; stu.email = ""
            ok2, m = database.add_student(stu)
            # If old DB function ignores section/phone, patch via SQL
            if ok2:
                con = sqlite3.connect(DB_NAME)
                cur = con.cursor()
                cur.execute("UPDATE students SET section=?, phone=? WHERE roll_no=?", (section, phone, roll))
                con.commit(); con.close()
            if ok2: messagebox.showinfo("Success", m); self.clear_add_form(); return
            else: messagebox.showerror("Error", m); return
        except Exception as e:
            # Direct SQL fallback - preserves old DB
            try:
                con = sqlite3.connect(DB_NAME)
                cur = con.cursor()
                cur.execute("INSERT INTO students (roll_no, name, course, section, phone, marks) VALUES (?,?,?,?,?,?)",
                            (roll, name, course, section, phone, marks))
                con.commit(); con.close()
                messagebox.showinfo("Success", "Student added successfully!"); self.clear_add_form()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"Roll Number {roll} already exists!")
            except Exception as ex:
                messagebox.showerror("Database Error", str(ex))

    def clear_add_form(self):
        self.cmb_course.set("Select Course")
        self.cmb_section.config(values=[], state="disabled"); self.cmb_section.set("Select Section - select course first")
        for e in [self.ent_name, self.ent_roll, self.ent_phone, self.ent_marks]: e.delete(0, tk.END)

    # ---------- 2. VIEW STUDENTS ----------
    def create_view_screen(self):
        f = tk.Frame(self.main, bg=BG)
        self.frames["view"] = f
        box = tk.LabelFrame(f, text="  View Students  ", bg=CARD_BG, fg=BLUE_DARK, font=("Segoe UI", 11, "bold"), padx=10, pady=10)
        box.pack(fill="both", expand=True)
        self.view_tree = self.make_table(box)

    def make_table(self, parent):
     cols = ("roll","name","course","section","phone","marks")
     container = tk.Frame(parent, bg=CARD_BG)
     container.pack(fill="both", expand=True)
     tree = ttk.Treeview(container, columns=cols, show="headings")
     for col, txt, w in [("roll","Roll Number",110),("name","Student Name",200),("course","Course",180),("section","Section",80),("phone","Phone",120),("marks","Marks",80)]:
        tree.heading(col, text=txt)
        tree.column(col, width=w, anchor="center" if col in ("roll","section","marks","phone") else "w")
     vs = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
     tree.configure(yscrollcommand=vs.set)
     tree.pack(side="left", fill="both", expand=True)
     vs.pack(side="right", fill="y")
     return tree

    def refresh_view_table(self):
        for i in self.view_tree.get_children(): self.view_tree.delete(i)
        try:
            rows = database.get_all_students()
        except:
            con = sqlite3.connect(DB_NAME); cur=con.cursor(); cur.execute("SELECT roll_no, name, course, section, phone, marks FROM students"); rows=cur.fetchall(); con.close()
        for r in rows:
            # r can be 4 or 7 columns
            if len(r) >= 6: self.view_tree.insert("", "end", values=(r[0], r[1], r[2], r[3] or "", r[4] or "", r[5]))
            elif len(r)==4: self.view_tree.insert("", "end", values=(r[0], r[1], r[2], "", "", r[3]))

    # ---------- 3. SEARCH SCREEN ----------
    def create_search_screen(self):
        f = tk.Frame(self.main, bg=BG)
        self.frames["search"] = f
        box = tk.LabelFrame(f, text="  Search Student  ", bg=CARD_BG, fg=BLUE_DARK, font=("Segoe UI", 11, "bold"), padx=12, pady=12)
        box.pack(fill="x")
        tk.Label(box, text="Search by Name or Roll Number", bg=CARD_BG, font=("Segoe UI", 10)).pack(anchor="w")
        row = tk.Frame(box, bg=CARD_BG); row.pack(fill="x", pady=8)
        self.ent_search = ttk.Entry(row, font=("Segoe UI", 11), width=35)
        self.ent_search.pack(side="left", padx=(0,8)); self.ent_search.bind("<Return>", lambda e: self.do_search())
        tk.Button(row, text="Search", bg=BLUE_DARK, fg="white", bd=0, padx=18, pady=6, command=self.do_search).pack(side="left", padx=4)
        tk.Button(row, text="Clear", bg="#64748B", fg="white", bd=0, padx=14, pady=6, command=self.clear_search).pack(side="left")

        res_box = tk.Frame(f, bg=BG); res_box.pack(fill="both", expand=True, pady=(12,0))
        self.search_tree = self.make_table(res_box)
        self.lbl_search_info = tk.Label(f, text="Enter name or roll number and click Search", bg=BG, fg="#64748B", font=("Segoe UI", 9))
        self.lbl_search_info.pack(pady=6)

    def do_search(self):
        q = self.ent_search.get().strip()
        if not q: messagebox.showwarning("Search", "Enter Roll Number or Name"); return
        for i in self.search_tree.get_children(): self.search_tree.delete(i)
        found=[]
        # Try roll
        try:
            r=int(q)
            try: row=database.search_student(r)
            except:
                con=sqlite3.connect(DB_NAME); cur=con.cursor(); cur.execute("SELECT roll_no, name, course, section, phone, marks FROM students WHERE roll_no=?", (r,)); row=cur.fetchone(); con.close()
            if row:
                if len(row)>=6: found=[(row[0],row[1],row[2],row[3] or "",row[4] or "",row[5])]
                else: found=[(row[0],row[1],row[2],"","",row[3])]
        except: pass
        if not found:
            try: rows=database.search_by_name(q) if hasattr(database,'search_by_name') else []
            except: rows=[]
            if not rows:
                con=sqlite3.connect(DB_NAME); cur=con.cursor()
                cur.execute("SELECT roll_no, name, course, section, phone, marks FROM students WHERE name LIKE ? OR CAST(roll_no AS TEXT) LIKE ?", (f"%{q}%", f"%{q}%")); rows=cur.fetchall(); con.close()
            for r in rows:
                if len(r)>=6: found.append((r[0],r[1],r[2],r[3] or "",r[4] or "",r[5]))
                else: found.append((r[0],r[1],r[2],"","",r[3]))
        if found:
            for r in found: self.search_tree.insert("", "end", values=r)
            self.lbl_search_info.config(text=f"Found {len(found)} result(s) for '{q}'", fg=BLUE_DARK)
        else:
            self.lbl_search_info.config(text=f"No match for '{q}'", fg="#DC2626")

    def clear_search(self):
        self.ent_search.delete(0, tk.END)
        for i in self.search_tree.get_children(): self.search_tree.delete(i)
        self.lbl_search_info.config(text="Enter name or roll number and click Search", fg="#64748B")

    # ---------- 4. STUDENT RECORDS - Course Wise ----------
    def create_records_screen(self):
        f = tk.Frame(self.main, bg=BG)
        self.frames["records"] = f
        # Two sub-screens in same frame
        self.records_cards_frame = tk.Frame(f, bg=BG)
        self.records_detail_frame = tk.Frame(f, bg=BG)

        # Cards header
        tk.Label(self.records_cards_frame, text="Select a Course", bg=BG, fg=BLUE_DARK, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,12))
        self.cards_grid = tk.Frame(self.records_cards_frame, bg=BG)
        self.cards_grid.pack(fill="both", expand=True)

        # Detail header
        top = tk.Frame(self.records_detail_frame, bg=BG); top.pack(fill="x", pady=(0,8))
        tk.Button(top, text="← Back to Courses", bg=CARD_BG, fg=BLUE_DARK, bd=1, padx=12, pady=5, cursor="hand2", command=self.show_course_cards).pack(side="left")
        self.lbl_course_title = tk.Label(top, text="", bg=BG, fg=BLUE_DARK, font=("Segoe UI", 12, "bold"))
        self.lbl_course_title.pack(side="left", padx=14)
        filt = tk.Frame(self.records_detail_frame, bg=CARD_BG, highlightbackground="#E2E8F0", highlightthickness=1)
        filt.pack(fill="x", pady=(0,8), padx=1)
        tk.Label(filt, text="Filter by Section:", bg=CARD_BG, font=("Segoe UI", 10)).pack(side="left", padx=12, pady=8)
        self.cmb_filter_sec = ttk.Combobox(filt, state="readonly", width=18, font=("Segoe UI", 10))
        self.cmb_filter_sec.pack(side="left", pady=8)
        self.cmb_filter_sec.bind("<<ComboboxSelected>>", self.filter_by_section)

        self.records_tree = self.make_table(self.records_detail_frame)
        self.lbl_records_info = tk.Label(self.records_detail_frame, text="", bg=BG, fg="#64748B"); self.lbl_records_info.pack(pady=6)

    def show_course_cards(self):
        self.records_detail_frame.pack_forget()
        self.records_cards_frame.pack(fill="both", expand=True)
        for w in self.cards_grid.winfo_children(): w.destroy()
        # Get counts from actual DB
        try: rows=database.get_all_students()
        except:
            con=sqlite3.connect(DB_NAME); cur=con.cursor(); cur.execute("SELECT course FROM students"); rows=cur.fetchall(); con.close(); rows=[(r[0],) for r in rows]
        counts={}
        for r in rows:
            c=r[2] if len(r)>2 else r[0]
            counts[c]=counts.get(c,0)+1
        # Show all COURSES as cards + any extra courses in DB
        all_courses = list(COURSES)
        for c in counts:
            if c not in all_courses: all_courses.append(c)
        cols=3
        for idx, course in enumerate(all_courses):
            card = tk.Frame(self.cards_grid, bg=CARD_BG, highlightbackground="#E2E8F0", highlightthickness=1, cursor="hand2")
            r,c = divmod(idx, cols)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="ew", ipady=10, ipadx=10)
            tk.Label(card, text=course, bg=CARD_BG, fg=BLUE_DARK, font=("Segoe UI", 10, "bold"), wraplength=180, justify="left").pack(pady=(12,4))
            tk.Label(card, text=f"{counts.get(course,0)} students", bg=CARD_BG, fg="#64748B", font=("Segoe UI", 9)).pack()
            tk.Button(card, text="View Students", bg=BLUE_PRIMARY, fg="white", bd=0, padx=14, pady=5, cursor="hand2", command=lambda cr=course: self.open_course(cr)).pack(pady=8)
        for i in range(cols): self.cards_grid.columnconfigure(i, weight=1)

    def open_course(self, course):
        self.current_course = course
        self.records_cards_frame.pack_forget()
        self.records_detail_frame.pack(fill="both", expand=True)
        self.lbl_course_title.config(text=course)
        secs = COURSE_SECTIONS.get(course, ["A","B","C"])
        # Check actual sections present
        try:
            con=sqlite3.connect(DB_NAME); cur=con.cursor(); cur.execute("SELECT DISTINCT section FROM students WHERE course=?", (course,)); db_secs=[s[0] for s in cur.fetchall() if s[0]]; con.close()
            for s in db_secs:
                if s not in secs: secs.append(s)
        except: pass
        self.cmb_filter_sec.config(values=["All Sections"]+secs); self.cmb_filter_sec.set("All Sections")
        self.load_course_students(course, "All Sections")

    def load_course_students(self, course, section_filter):
        for i in self.records_tree.get_children(): self.records_tree.delete(i)
        try:
            con=sqlite3.connect(DB_NAME); cur=con.cursor()
            if section_filter=="All Sections": cur.execute("SELECT roll_no, name, course, section, phone, marks FROM students WHERE course=?", (course,))
            else: cur.execute("SELECT roll_no, name, course, section, phone, marks FROM students WHERE course=? AND section=?", (course, section_filter))
            rows=cur.fetchall(); con.close()
        except:
            rows=[]
        if not rows:
            self.lbl_records_info.config(text=f"No students registered in {course}" + (f" - Section {section_filter}" if section_filter!="All Sections" else ""), fg="#DC2626")
        else:
            for r in rows: self.records_tree.insert("", "end", values=(r[0],r[1],r[2],r[3] or "",r[4] or "",r[5]))
            self.lbl_records_info.config(text=f"{len(rows)} student(s) in {course}", fg=BLUE_DARK)

    def filter_by_section(self, e=None):
        self.load_course_students(self.current_course, self.cmb_filter_sec.get())

if __name__ == "__main__":
    ensure_schema()
    root = tk.Tk()
    App(root)
    root.mainloop()

