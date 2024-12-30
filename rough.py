            
            
import customtkinter as ctk
import pandas as pd
from datetime import datetime
from tkinter import messagebox, simpledialog, IntVar
from tkcalendar import Calendar




class AttendanceSystem:
    
    
    
    
    def __init__(self):
        self.attendance_data = {} 
        self.marks_data = {} 
    
    
    
    
    def export_marks_to_csv(self, subject, username ):
        records = []

        filename=f'{username}_{subject}.csv'
        for student_id, data in self.marks_data.items():
            for subject, marks in data['marks'].items():
                records.append([student_id, data['name'], subject, marks])
        df = pd.DataFrame(records, columns=['Student ID', 'Name', 'Subject', 'Marks'])
        df.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Marks data exported to {filename}")
    
    
    
    
    def add_students(self, students):
        success_messages = []
        for student_id, student_name in students:
            if student_id not in self.attendance_data:
                self.attendance_data[student_id] = {
                    'name': student_name,
                    'attendance': {}
                }
                self.marks_data[student_id] = {
                    'name': student_name,
                    'marks': {}
                }
                success_messages.append(f"Student {student_name} with ID {student_id} added successfully.")
            else:
                messagebox.showwarning("Error", f"Student {student_id} already exists.")
        if success_messages:
            messagebox.showinfo("Success", "\n".join(success_messages))
    
    
    
    
    
    def mark_attendance(self, main_frame, date=None ):
        '''if date is None:
            date = datetime.today().strftime("%Y-%m-%d")
            print("today date", date)'''
        student_vars = {}
        for widget in main_frame.winfo_children():
            widget.destroy()
        
        
        
        
        def on_date_submit():
            select_date = cal.selection_get()
            nonlocal date
            date = select_date.strftime("%d-%m-%Y")
            print("formated date :",date)
            mark_attendance_for_date(date)
            
        
        
        
        
        def mark_attendance_for_date(date):
            for widget in main_frame.winfo_children():
                widget.destroy()
            student_vars.clear()
            ctk.CTkLabel(main_frame, text=f"Mark Attendance for {date} \n formate MM-DD-YYYY", font=('Helvetica', 16)).pack(pady=20)
            for student_id, data in self.attendance_data.items():
                var = IntVar()
                student_vars[student_id] = var
                cb = ctk.CTkCheckBox(main_frame, text=data['name'], variable=var)
                cb.pack(anchor='w')
            save_button = ctk.CTkButton(main_frame, text="Save", command=save_attendance, width=20)
            save_button.pack(pady=10)
            back_button = ctk.CTkButton(main_frame, text="Back", command=lambda: show_teacher_menu, width=20)
            back_button.pack(pady=10)

        
        
        
        ctk.CTkLabel(main_frame, text="Select the date (DD-MM-YYYY)", font=('Helvetica', 16)).pack(pady=20)
        today = datetime.today()
        cal = Calendar(main_frame, selectmode='day',  year=today.year, month=today.month, day=today.day)
        cal.pack(pady=20)
        cal.bind("<<CalendarSelected>>", lambda event :on_date_submit)
        for detail in details:
                if detail[0] == username :

                    global subject                                                  # >>>>>>>>>> Teacher subject
                    subject = detail[2]
                    break 


        
        
        submit_button = ctk.CTkButton(main_frame, hover_color="#008744",text="Submit Date", command=on_date_submit, width=20)# green color 
        submit_button.pack(pady=10)
        ctk.CTkButton(main_frame, text="Back", command=lambda : show_teacher_menu(details,root, main_frame, subject), height=30, width = 100, corner_radius= 15,hover_color="#ff0000",anchor="s").pack(pady=10)
        ctk.CTkButton(main_frame, text="Home", command=lambda: show_login_menu(root, main_frame), height=30, width = 100, corner_radius= 15,hover_color="#ff0000",anchor="s").pack(pady=10)

        
        
        
        
        
        def save_attendance():
            for detail in details:
                if detail[0] == username :

                    global subject                                                  # >>>>>>>>>> Teacher subject
                    subject = detail[2]
                    break 
                
            for student_id, var in student_vars.items():
                status = 'P' if var.get() == 1 else 'A'
                self.attendance_data[student_id]['attendance'][date] = status
            messagebox.showinfo("Success", "Attendance marked successfully!")
            show_teacher_menu(details,root, main_frame, subject)
            
            attendance_system.export_attendance_to_csv(details)
    
    
    
    
    
    def export_attendance_to_csv(self,details):
        filename=f"{username}.csv"
        records = []
        for student_id, data in self.attendance_data.items():
            for date, status in data['attendance'].items():
                records.append([student_id, data['name'], date, status])

        df = pd.DataFrame(records, columns=['Student ID', 'Name', 'Date', 'Status'])
        df.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Attendance data exported to {filename}")

    
    
    
    
    
    def read_csv_to_dict(self):
        file_path = f'{username}.csv'
        df = pd.read_csv(file_path)
        expected_columns = {'Student ID', 'Name', 'Date', 'Status'}
        if not expected_columns.issubset(set(df.columns)):
            raise ValueError(f"CSV file does not contain the required columns: {expected_columns}")
        global attendance_dict
        attendance_dict = {}
        for _, row in df.iterrows():
            student_id = row['Student ID']
            name = row['Name']
            date = row['Date']
            status = row['Status']
            if student_id not in attendance_dict:
                attendance_dict[student_id] = {'name': name, 'attendance': {}}
            attendance_dict[student_id]['attendance'][date] = status

        return attendance_dict
        

    
    
    
    def get_attendance(self, student_id, year, month):
        print(attendance_dict)

        try:
            student_id = int(student_id)
            year = int(year)
            month = int(month)
        except ValueError:
            messagebox.showwarning("Error", "Student ID, Year, and Month should be numbers.")
            return


        if student_id in attendance_dict:
            name = attendance_dict[student_id]['name']
            attendance_records = attendance_dict[student_id]['attendance']
            filtered_records = {date: status for date, status in attendance_records.items() if datetime.strptime(date, '%d-%m-%Y').year == year and datetime.strptime(date, '%d-%m-%Y').month == month}
            messagebox.showinfo(f"Name: {name}\nStudent ID: {student_id}\n", filtered_records)
        else:
            messagebox.showwarning("Error", f"No records found for student ID {student_id}")
            return None, {}
    
    
    
    
    
    def update_marks(self, subject , username):

          
        def save_marks():


                       
            for student_id, entry in entries.items():
                
                marks = entry.get()
                if subject and marks:
                    self.marks_data[student_id]['marks'][subject] = int(marks)
            messagebox.showinfo("Success", "Marks updated successfully!")
            attendance_system.export_marks_to_csv(subject , username)

        for widget in main_frame.winfo_children():
            widget.destroy()

                      
        ctk.CTkLabel(main_frame, text=f"Update Marks   \nsubject :{subject}").pack(pady=20)


        
        entries = {}

        for student_id, data in self.marks_data.items():
            ctk.CTkLabel(main_frame, text=data['name']).pack(anchor='w')
            entry = ctk.CTkEntry(main_frame)
            entry.pack(anchor='w')
            entries[student_id] = entry
        save_button = ctk.CTkButton(main_frame, text="Save", command=save_marks)
        save_button.pack()
        back_button = ctk.CTkButton(main_frame, text="Back", command=lambda: show_teacher_menu(details,root, main_frame, subject))
        back_button.pack()





class Teacher:
    def __init__(self, username):
        self.username = username






def teacher_login(details, root, main_frame):
    global username
    username = username_entry.get()
    global password
    password = password_entry.get()
    subject = None

    for detail in details:
        if detail[0] == username and detail[1] == password:
            subject = detail[2]
            break
        
    if subject is not None:# # Initialize AttendanceSystem with userna
        teacher = Teacher(username)
        messagebox.showinfo("Welcome", f"Welcome Teacher {username}  your are the  {subject} teacher of Sec 10")
        show_teacher_menu(details,root, main_frame,subject)
    else:
        messagebox.showerror("Error", "Invalid login credentials")





def show_teacher_menu(details,root, main_frame, subject):
    for widget in main_frame.winfo_children():
        widget.destroy()
    def on_mark_attendance():
        attendance_system.mark_attendance(main_frame)
    def on_check_attendance():
        for widget in main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(main_frame, text="Check Attendance", font=('Helvetica', 16)).pack(pady=20)
        student_id_label = ctk.CTkLabel(main_frame, text="Student ID")
        student_id_label.pack()
        global student_id_entry
        student_id_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter Student ID")
        student_id_entry.pack(pady=5)
        
        year_label = ctk.CTkLabel(main_frame, text="Year")
        year_label.pack()

        global year_entry
        year_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter Year (YYYY)")
        year_entry.pack(pady=5)
        
        month_label = ctk.CTkLabel(main_frame, text="Month")
        month_label.pack()
        
        global month_entry
        month_entry = ctk.CTkEntry(main_frame, placeholder_text="Enter Month (MM)")
        month_entry.pack(pady=5)               

        
        ctk.CTkButton(main_frame, text="Check Attendance", height=30, width = 80, corner_radius= 15,hover_color="#ffa700", command= fetch_att).pack(pady=10)
        ctk.CTkButton(main_frame, text="Back", height=20, width = 40, corner_radius= 15,hover_color="#ff0000", command=lambda: show_teacher_menu(details,root, main_frame, subject)).pack(pady=5)
        ctk.CTkButton(main_frame, text="Home", height=20, width = 40, corner_radius= 15,hover_color="#ff0000", command=lambda: show_login_menu(root, main_frame)).pack(pady=5)


    
    
    def fetch_att():
        attendance_system.read_csv_to_dict()
        attendance_system.get_attendance(student_id_entry.get(), year_entry.get(), month_entry.get())

        
    
    
    def on_update_marks():

        for detail in details:
                if detail[0] == username and detail[1] == password:
                    
                    subject = detail[2]
                    break
        attendance_system.update_marks(subject , username)

    
    
    
    def on_check_marks():
        student_id = simpledialog.askinteger("Input", "Enter the student ID to check marks:")
        if student_id in attendance_system.marks_data:
            marks_records = attendance_system.marks_data[student_id]['marks']
            records_str = "\n".join([f"Subject: {subject}, Marks: {marks}" for subject, marks in marks_records.items()])
            messagebox.showinfo("Marks Records", records_str)
        else:
            messagebox.showwarning("Error", f"No records found for student ID {student_id}")

    
    
    
    def on_add_students():
        students = []
        while True:
            student_id = simpledialog.askinteger("Input", "Enter the student ID to add (or Cancel to stop):")
            if student_id is None:
                break
            name = simpledialog.askstring("Input", "Enter the name of the student:")
            if name is None:
                break
            students.append((student_id, name))
        attendance_system.add_students(students)

    for detail in details:
        
        if detail[0] == username_entry and detail[1] == password_entry:
            subject = detail[2]
            break
               

    ctk.CTkLabel(main_frame, text= f"Teacher Menu \n \n Teacher Name : {username} \n \n Teacher's subject : {subject}", font=('Helvetica', 16), height=30, width = 250, corner_radius= 15).pack(pady=20)
    ctk.CTkButton(main_frame, text="Mark Attendance", command=on_mark_attendance, height=30, width = 250, corner_radius= 15,hover_color="#ffa700").pack(pady=10)
    ctk.CTkButton(main_frame, text="Check Student Attendance", command=on_check_attendance, height=30, width = 250, corner_radius= 15,hover_color="#ffa700").pack(pady=10)
    ctk.CTkButton(main_frame, text="Give Marks to Students", command=on_update_marks, height=30, width = 250, corner_radius= 15,hover_color="#ffa700").pack(pady=10)
    ctk.CTkButton(main_frame, text="Check Student Marks", command=on_check_marks, height=30, width = 250, corner_radius= 15,hover_color="#ffa700").pack(pady=10)
    ctk.CTkButton(main_frame, text="Add Students", command=on_add_students, height=30, width = 250, corner_radius= 15,hover_color="#ffa700").pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", command=lambda: show_login_menu(root, main_frame), height=20, width = 40, corner_radius= 15,hover_color="#ff0000",anchor="s").pack(pady=10)
    ctk.CTkButton(main_frame, text="Home", command=lambda: show_login_menu(root, main_frame), height=20, width = 40, corner_radius= 15,hover_color="#ff0000",anchor="s").pack(pady=10)




def show_login_menu(root, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    root.title("Galgotias Login Page")
    def on_teacher_login():
        show_teacher_login_form(root, main_frame)
    def on_student_login():
        show_student_login_form(root, main_frame)
    ctk.CTkLabel(main_frame, text="Welcome to the Galgotias login page", font=('Helvetica', 16)).pack(pady=10)
    ctk.CTkButton(main_frame, text="Teacher Login", command=on_teacher_login, width=20, hover_color="#fa7e1e").pack(pady=10)
    ctk.CTkButton(main_frame, text="Student Login", command=on_student_login, width=20,hover_color="#fa7e1e").pack(pady=10)
    ctk.CTkButton(main_frame, text="Exit", command=root.quit, width=20,hover_color="#ff0000",anchor="s").pack(pady=10)





def show_teacher_login_form(root, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    ctk.CTkLabel(main_frame, text="Teacher Login", font=('Helvetica', 16)).pack(pady=20)



    
    global username_entry
    username_entry = ctk.CTkEntry(main_frame,placeholder_text="username")
    username_entry.pack(pady=5)
    
    global password_entry
    password_entry = ctk.CTkEntry(main_frame,placeholder_text="Password", show='*')
    password_entry.pack(pady=5)
    ctk.CTkButton(main_frame, text="Login", height=25, width = 80, corner_radius= 15,hover_color="#008744",command=lambda: teacher_login(details, root, main_frame)).pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", height=20, width = 40, corner_radius= 15 ,hover_color="#ff0000",command=lambda: show_login_menu(root, main_frame)).pack()
    ctk.CTkButton(main_frame, text="Home", height=20, width = 40, corner_radius= 15,hover_color="#ff0000", command=lambda: show_login_menu(root, main_frame)).pack(pady=10)




def show_student_login_form(root, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    ctk.CTkLabel(main_frame, text="Student Login", font=('Helvetica', 16)).pack(pady=20)
    ctk.CTkLabel(main_frame, text="Username:").pack(pady=5)
    global username_entry
    username_entry = ctk.CTkEntry(main_frame)
    username_entry.pack(pady=5)
    ctk.CTkLabel(main_frame, text="Password:").pack(pady=5)
    global password_entry
    password_entry = ctk.CTkEntry(main_frame, show='*')
    password_entry.pack(pady=5)
    ctk.CTkButton(main_frame, text="Login", command=lambda: student_login(details, root, main_frame), width=20).pack(pady=10)
    ctk.CTkButton(main_frame, text="Back", command=lambda: show_login_menu(root, main_frame), width=20).pack(pady=10)
    ctk.CTkButton(main_frame, text="Home", command=lambda: show_login_menu(root, main_frame), width=20).pack(pady=10)




def student_login(details, root, main_frame):   #in future the options will added 
    pass





if __name__ == "__main__":

    global details
    details = [["akshat", "123","Python"], ["abhinandan", "234", "Maths"],["Bhavya", "345", "edp"]]


    
   

    
    
    attendance_system = AttendanceSystem()

    attendance_system.add_students([(1, 'Akshat Raj'), (2, 'Abhinandan Kumar'), (3,'Arpit '),(4, 'Aman Kumar'), (5,'Abhishek'),(6, 'Abhinav Kumar'),(7,'Aakash'), (8, 'Aniket Singh Thakur'),(9,'Aniket pandey'),(10,'Anubhav kumar'),(11,'Anurag'),(12,'Arnav'),(13,'Alok kumar'),(14,'Bhavya Garga'),(15,'Devendra '),(16,'Deepanshu'),(17,'Gagan'),(18,'Himanshu'),(19,'Hamant'),(20,'keshav'),(21,'kumar Mangalam'),(22,'Piyush'),(23,'Nikhil'),(24,'Somil'),(25,'Saurabh '),(26,'Swaraj'),(27,"Sarthak kumar"),(28,'Naman'),(29,'Raman kumar'),(30,'Rahul')])

    root = ctk.CTk()
    

    root._set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root.geometry("500x500")
    

    
    main_frame = ctk.CTkScrollableFrame(master=root, height= 300, width =300 ,border_width=5 , border_color= "#97ebdb", scrollbar_button_color="#97ebdb" , scrollbar_button_hover_color="#ff71ce" , fg_color="#343d46")
    main_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    show_login_menu(root, main_frame)
    root.mainloop()
