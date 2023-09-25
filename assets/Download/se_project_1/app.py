import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import Text
import os
import json
import string
import re
import sys

# constants
SELECTED_HEIGHT = 5
NON_SELECTED_HEIGHT = 3
WIDTH = 20
# IF you add a new button, you need to add the name in order below, 
# and change indexes in def create_panel_for_button.

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle/exe
    CURRENT_DIR = os.path.dirname(sys.executable)
else:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

BUTTON_TEXTS = ["Add new user", "Update user", "Display all", "Search"]
EMPLOYEE_JSON = os.path.join(CURRENT_DIR, "employees.json")
EULA_AGREEMENT_TEXT = os.path.join(CURRENT_DIR, "eulaagreement.txt")
EULA_VERIFICATION = os.path.join(CURRENT_DIR, "eula.txt")
# create_main, load_employees, and buttons functions
# employees.json structure created by Drew Penn
def create_main_window():
    root = tk.Tk()
    root.title("SE project 1 - group 2")
    root.geometry('600x800')
    return root

def load_employees():
    with open(EMPLOYEE_JSON, 'r') as f:
        data = json.load(f)
    
    #print(data)
    return data["employees"]

def on_button_click(clicked_index, buttons, panel):
    # Iterating over all buttons, find the one that is clicked, adjust size
    for index, button in enumerate(buttons):
        if index == clicked_index:
            button.config(height=SELECTED_HEIGHT, width=WIDTH)
        else:
            button.config(height=NON_SELECTED_HEIGHT, width=WIDTH)

    create_panel_for_button(clicked_index, panel)

def create_buttons(frame, panel):
    buttons = []
    for i, text in enumerate(BUTTON_TEXTS):
        btn = tk.Button(frame, text=text, height=NON_SELECTED_HEIGHT, width=WIDTH,
                        command=lambda i=i: on_button_click(i, buttons, panel))
        btn.grid(row=1, column=i,sticky="s")
        buttons.append(btn)
    buttons[0].config(height=SELECTED_HEIGHT, width=WIDTH)  # default button
    return buttons

def create_panel_for_button(index, panel):
    for widget in panel.winfo_children():
        widget.destroy()

    if index == 0:      # Add new user
        add_new_user_panel(panel)
    elif index == 1:    # Update all
        add_update_panel(panel)
    elif index == 2:    # Display all
        add_display_panel(panel)
    else:               # Search
        add_search_panel(panel)

def check_special_chars(entry):
        """
        This function accepts any "entry" or inputbox, checks if it has a 
        special character. If it does, changes color, if not, stays white.
        """
        content = entry.get()
        # Check if there are any special characters in the content
        if any(char in string.punctuation for char in content):
            entry.config(bg="mistyrose")
        else:
            entry.config(bg="white")
    
# new user panel done by Drew Penn
def add_new_user_panel(panel):
    """
    This function will layout the panel in the following order:
    first name
    last name
    phone number
    (others)

    each input box is checked for special characters, if it has any, it will turn red.
    """
    def format_phone_number(event=None):
        """
        When the phone number input box is unfocused, it cleans the input of hyphens,
        verifies if it is 10 digits, if it is it adds hyphens if it isn't it turns red.
        """
        content = phone_entry.get()
        # Remove any hyphens that user might have entered
        clean_content = content.replace("-", "")

        if len(clean_content) == 10 and clean_content.isdigit():
            formatted_num = clean_content[:3] + "-" + clean_content[3:6] + "-" + clean_content[6:]
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, formatted_num)
            phone_entry.config(bg="white")  # Reset to normal background color
        elif content:
            phone_entry.config(bg="mistyrose")  # Invalid input

    def format_email(event=None):
        content = email_entry.get()

        # A simple regular expression for email validation
        # This pattern checks for [some chars]@[some chars].[some chars]
        # This is a basic validation and might not capture all edge cases
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")

        if email_pattern.match(content):
            email_entry.config(bg="white")  
        else:
            email_entry.config(bg="mistyrose")  

    def format_SSN(event=None):
        """
        This does the same thing as the format_phone_number but for the SSN
        """
        content = ssn_entry.get()
        # Remove any hyphens that user might have entered
        clean_content = content.replace("-", "")

        if len(clean_content) == 9 and clean_content.isdigit():
            formatted_ssn = clean_content[:3] + "-" + clean_content[3:5] + "-" + clean_content[5:]
            ssn_entry.delete(0, tk.END)
            ssn_entry.insert(0, formatted_ssn)
            ssn_entry.config(bg="white")  
        elif content:
            ssn_entry.config(bg="mistyrose")  

    
    # Create a sub-frame to contain the labels and entry widgets
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    #sub_frame.config(text="")
    sub_frame.pack(pady=20)

    instructions = tk.Label(sub_frame, text="Please fill out all the following fields. Do not use special characters. If there is an issue, the field will turn red.")
    instructions.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # First name label and entry
    first_name_label = tk.Label(sub_frame, text="First Name:")
    first_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    first_name_entry = tk.Entry(sub_frame)
    first_name_entry.bind("<FocusOut>", lambda event, entry=first_name_entry: check_special_chars(entry))
    first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    # Last name label and entry
    last_name_label = tk.Label(sub_frame, text="Last Name:")
    last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    last_name_entry = tk.Entry(sub_frame)
    last_name_entry.bind("<FocusOut>", lambda event, entry=last_name_entry: check_special_chars(entry))
    last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Phone number label and entry
    phone_label = tk.Label(sub_frame, text="Phone Number:")
    phone_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
    phone_entry = tk.Entry(sub_frame)
    phone_entry.bind("<FocusOut>", format_phone_number)
    phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    # Email address label and entry
    email_label = tk.Label(sub_frame, text="Email Address:")
    email_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
    email_entry = tk.Entry(sub_frame)
    email_entry.bind("<FocusOut>", format_email)
    email_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    # Home address label and entry
    home_address_label = tk.Label(sub_frame, text="Home Address:")
    home_address_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
    home_address_entry = tk.Entry(sub_frame)
    home_address_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    # SSN label and entry
    ssn_label = tk.Label(sub_frame, text="SSN:")
    ssn_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
    ssn_entry = tk.Entry(sub_frame)
    ssn_entry.bind("<FocusOut>", format_SSN)
    ssn_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

    # Skills label and entry
    skills_label = tk.Label(sub_frame, text="Skills (comma delineated ex:Fishing, hunting):")
    skills_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
    skills_entry = tk.Entry(sub_frame)
    skills_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

    # Position label and entry
    position_label = tk.Label(sub_frame, text="Position:")
    position_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
    position_entry = tk.Entry(sub_frame)
    position_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)
    
    def check_errors_and_submit():
    # Check for errors
        for widget in sub_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                    if widget.cget('bg') == 'mistyrose' or not widget.get().strip():
                        messagebox.showerror("Error", "Fix the red entry boxes or fill empty fields")
                        return

        full_name = first_name_entry.get() + " " + last_name_entry.get()

        # Collect data and append to JSON
        new_employee = {
            "uid": generate_uid(),
            "name": full_name,
            "position": position_entry.get(),
            "ssn": ssn_entry.get(),
            "address": home_address_entry.get(),
            "email": email_entry.get(),
            "phonenumber": phone_entry.get(),
            "skills": skills_entry.get()
        }

        with open(EMPLOYEE_JSON, 'r+') as f:
            data = json.load(f)
            data["employees"].append(new_employee)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def generate_uid():
        with open(EMPLOYEE_JSON, 'r') as f:
            data = json.load(f)
            max_uid = max([emp["uid"] for emp in data["employees"]])
        return max_uid + 1

    # Submit button
    submit_btn = tk.Button(sub_frame, text="Submit", command=check_errors_and_submit)
    submit_btn.grid(row=9, column=1, padx=5, pady=5)

    return

# add_update_panel completed by Nguyen Do
def add_update_panel(panel):
    my_employees = load_employees()

    def get_employee_data(uid, employees):
        for employee in employees:
            if employee['uid'] == uid:
                return employee


    def show_user_selection():
        def on_select():
            global selected_uid
            
            selected_data = users_listbox.get(users_listbox.curselection())
            uid_str = selected_data.split(':')[0].strip()  # Split the string at ':' and get the UID part
            selected_uid = int(uid_str)  # Convert the UID part to an integer

            grab_user_data()
            user_selection_window.destroy()

        user_selection_window = tk.Toplevel(panel)
        user_selection_window.title("Select User to Update")

        users_listbox = tk.Listbox(user_selection_window)
        for emp in load_employees():
            users_listbox.insert(tk.END, str(emp["uid"]) + ": " + emp["name"])
        users_listbox.pack(pady=20, padx=20)

        select_btn = tk.Button(user_selection_window, text="Select", command=on_select)
        select_btn.pack(pady=10)

    def grab_user_data():
        """Populate the fields with selected user data after selecting from the list."""
        employee = get_employee_data(selected_uid, my_employees)

        # Populate the text fields with user's data
        first_name_entry.delete(0, tk.END)
        first_name_entry.insert(0, employee["name"].split()[0])
        
        last_name_entry.delete(0, tk.END)
        last_name_entry.insert(0, employee["name"].split()[1] if len(employee["name"].split()) > 1 else "")
        
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, employee["phonenumber"])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, employee["email"])

        home_address_entry.delete(0, tk.END)
        home_address_entry.insert(0, employee["address"])

        ssn_entry.delete(0, tk.END)
        ssn_entry.insert(0, employee["ssn"])

        skills_entry.delete(0, tk.END)
        skills_entry.insert(0, employee["skills"])

        position_entry.delete(0, tk.END)
        position_entry.insert(0, employee["position"])

    def format_phone_number(event=None):
        """
        When the phone number input box is unfocused, it cleans the input of hyphens,
        verifies if it is 10 digits, if it is it adds hyphens if it isn't it turns red.
        """
        content = phone_entry.get()
        # Remove any hyphens that user might have entered
        clean_content = content.replace("-", "")

        if len(clean_content) == 10 and clean_content.isdigit():
            formatted_num = clean_content[:3] + "-" + clean_content[3:6] + "-" + clean_content[6:]
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, formatted_num)
            phone_entry.config(bg="white")  # Reset to normal background color
        elif content:
            phone_entry.config(bg="mistyrose")  # Invalid input

    def format_email(event=None):
        content = email_entry.get()

        # A simple regular expression for email validation
        # This pattern checks for [some chars]@[some chars].[some chars]
        # This is a basic validation and might not capture all edge cases
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")

        if email_pattern.match(content):
            email_entry.config(bg="white")  
        else:
            email_entry.config(bg="mistyrose")  

    def format_SSN(event=None):
        """
        This does the same thing as the format_phone_number but for the SSN
        """
        content = ssn_entry.get()
        # Remove any hyphens that user might have entered
        clean_content = content.replace("-", "")

        if len(clean_content) == 9 and clean_content.isdigit():
            formatted_ssn = clean_content[:3] + "-" + clean_content[3:5] + "-" + clean_content[5:]
            ssn_entry.delete(0, tk.END)
            ssn_entry.insert(0, formatted_ssn)
            ssn_entry.config(bg="white")  
        elif content:
            ssn_entry.config(bg="mistyrose")  
        
    # Place the Grab User button at the top
    grab_user_btn = tk.Button(panel, text="Click here to grab employee info", command=show_user_selection)
    grab_user_btn.pack(pady=10)

     # Create a sub-frame to contain the labels and entry widgets
    sub_frame = tk.Frame(panel, bg=panel.cget('bg'))
    #sub_frame.config(text="")
    sub_frame.pack(pady=20)


    # First name label and entry
    first_name_label = tk.Label(sub_frame, text="First Name:")
    first_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    first_name_entry = tk.Entry(sub_frame)
    first_name_entry.bind("<FocusOut>", lambda event, entry=first_name_entry: check_special_chars(entry))
    first_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    # Last name label and entry
    last_name_label = tk.Label(sub_frame, text="Last Name:")
    last_name_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    last_name_entry = tk.Entry(sub_frame)
    last_name_entry.bind("<FocusOut>", lambda event, entry=last_name_entry: check_special_chars(entry))
    last_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Phone number label and entry
    phone_label = tk.Label(sub_frame, text="Phone Number:")
    phone_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
    phone_entry = tk.Entry(sub_frame)
    phone_entry.bind("<FocusOut>", format_phone_number)
    phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    # Email address label and entry
    email_label = tk.Label(sub_frame, text="Email Address:")
    email_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
    email_entry = tk.Entry(sub_frame)
    email_entry.bind("<FocusOut>", format_email)
    email_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    # Home address label and entry
    home_address_label = tk.Label(sub_frame, text="Home Address:")
    home_address_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
    home_address_entry = tk.Entry(sub_frame)
    home_address_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    # SSN label and entry
    ssn_label = tk.Label(sub_frame, text="SSN:")
    ssn_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
    ssn_entry = tk.Entry(sub_frame)
    ssn_entry.bind("<FocusOut>", format_SSN)
    ssn_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

    # Skills label and entry
    skills_label = tk.Label(sub_frame, text="Skills (comma delineated ex:Fishing, hunting):")
    skills_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
    skills_entry = tk.Entry(sub_frame)
    skills_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

    # Position label and entry
    position_label = tk.Label(sub_frame, text="Position:")
    position_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
    position_entry = tk.Entry(sub_frame)
    position_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

    def check_errors_and_submit():
        # Check for errors
        for widget in sub_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                    if widget.cget('bg') == 'mistyrose' or not widget.get().strip():
                        messagebox.showerror("Error", "Fix the red entry boxes or fill empty fields")
                        return

        full_name = first_name_entry.get() + " " + last_name_entry.get()

        # Collect data and append to JSON
        updated_employee = get_employee_data(selected_uid, my_employees)

        updated_employee = {
            "uid": selected_uid,
            "name": full_name,
            "position": position_entry.get(),
            "ssn": ssn_entry.get(),
            "address": home_address_entry.get(),
            "email": email_entry.get(),
            "phonenumber": phone_entry.get(),
            "skills": skills_entry.get()
        }

        with open(EMPLOYEE_JSON, 'r+') as f:
            data = json.load(f)

            # this finds the employee with the matching UID and update details
            for index, employee in enumerate(data["employees"]):
                if employee["uid"] == selected_uid:
                    data["employees"][index] = updated_employee
                    break
            else:
                # if no matching UID is found this append the new employee to the list.
                data["employees"].append(updated_employee)

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()


    # Place the Update button at the bottom
    update_btn = tk.Button(panel, text="Update", command=check_errors_and_submit)
    update_btn.pack(pady=20)

    return

def add_display_panel(panel):

    def display_selected_info():
        # Clear the text_area
        text_area.delete(1.0, tk.END)

        for employee in employees:
            for key, value in employee.items():
                if vars_dict[key].get():
                    text_area.insert(tk.END, f"{key}: {value}\n")
            text_area.insert(tk.END, "\n")
    
    # loading employees and creating a dict for buttons to be added to
    employees = load_employees()
    vars_dict = {}

    instructions_label = tk.Label(panel, text="Select the fields you would like to query and display the contents of.")
    instructions_label.pack(pady=10)

    checkbox_frame = tk.Frame(panel)
    checkbox_frame.pack(pady=20)

    # Dynamically creates checkboxes per the contents of the employees.json
    # making them dynamic fields that would expand withotu 
    for index, key in enumerate(employees[0].keys()):
        display_key = key.capitalize()
        vars_dict[key] = tk.IntVar()
        chk = tk.Checkbutton(checkbox_frame, text=display_key, variable=vars_dict[key])
        chk.grid(row=index, column=0, sticky=tk.W, padx=10, pady=2)
    
    display_button = tk.Button(panel, text="Display All", command=display_selected_info)
    display_button.pack(pady=10)

    text_area = tk.Text(panel, wrap=tk.WORD, width=70, height=40)
    text_area.pack(padx=10, pady=10)

    return


#search function/Window
#by Andreh N And Lilac S

def add_search_panel(panel):
    #def search
    def perform_search():
        search_text = search_entry.get().strip()
        #ignore dashes,space, and ()
        search_text = search_text.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        results = []
        
        #employee data from the JSON fileS
        employees = load_employees()

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        selected_option = selected_option_var.get()
        

        if selected_option == "All":
            results = [emp for emp in employees if search_text.lower() in str(emp).lower()
                       .replace(' ', '').replace('-', '').replace('(', '').replace(')', '')]#ignore dashes,spaces, and ()

        elif selected_option == "Name":
            results = [emp for emp in employees if search_text.lower() in emp["name"].lower()]
        elif selected_option == "Address":
            results = [emp for emp in employees if search_text.lower() in emp["address"].lower()]
        elif selected_option == "SSN":
            results = [emp for emp in employees if search_text in emp["ssn"]
                       .replace(' ', '').replace('-', '').replace('(', '').replace(')', '')]#ignore dashes,spaces, and ()
        elif selected_option == "Email":
            results = [emp for emp in employees if search_text.lower() in emp["email"].lower()]
        elif selected_option == "Skills":
            results = [emp for emp in employees if search_text.lower() in emp["skills"].lower()]
        elif selected_option == "Phone Number": 
            results = [emp for emp in employees if search_text in emp["phonenumber"]
                       .replace(' ', '').replace('-', '').replace('(', '').replace(')', '')] #ignore dashes,spaces, and ()
        elif selected_option == "Position":
            results = [emp for emp in employees if search_text.lower() in emp["position"].lower()]  

            
        display_search_results(results , selected_option)


    #default to all button at start
    selected_option_var = tk.StringVar()
    selected_option_var.set("All")

    
    all_var = tk.BooleanVar()
    name_var = tk.BooleanVar()
    address_var = tk.BooleanVar()
    ssn_var = tk.BooleanVar()
    email_var = tk.BooleanVar()  
    skills_var = tk.BooleanVar()
    phonenumber_var = tk.BooleanVar()
    position_var = tk.BooleanVar()


    #radio buttons
    all_radio = tk.Radiobutton(panel, text="All", variable=selected_option_var, value="All")
    name_radio = tk.Radiobutton(panel, text="Name", variable=selected_option_var, value="Name")
    address_radio = tk.Radiobutton(panel, text="Address", variable=selected_option_var, value="Address")
    ssn_radio = tk.Radiobutton(panel, text="SSN", variable=selected_option_var, value="SSN")
    email_radio = tk.Radiobutton(panel, text="Email", variable=selected_option_var, value="Email")
    skills_radio = tk.Radiobutton(panel, text="Skills", variable=selected_option_var, value="Skills")
    phonenumber_radio = tk.Radiobutton(panel, text="Phone Number", variable=selected_option_var, value="Phone Number")
    position_radio = tk.Radiobutton(panel, text="Position", variable=selected_option_var, value="Position")

    #vertical set for buttons
    all_radio.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    name_radio.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    address_radio.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    ssn_radio.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    email_radio.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
    skills_radio.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
    phonenumber_radio.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
    position_radio.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    # Search bar
    search_label = tk.Label(panel, text="Search:")
    search_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)

    search_entry = tk.Entry(panel)
    search_entry.grid(row=9, column=0, padx=10, pady=5, sticky=tk.W + tk.E)

    search_button = tk.Button(panel, text="Search", command=perform_search)
    search_button.grid(row=9, column=1, padx=10, pady=5, sticky=tk.W)

    # result window
    result_label = tk.Label(panel, text="Search Results:")
    result_label.grid(row=10, column=0, padx=10, pady=5, sticky=tk.W)

    result_text = tk.Text(panel, height=15, width=70 ,state=tk.DISABLED , wrap=tk.NONE)
    result_text.grid(row=11, column=0, padx=10, pady=5, columnspan=2, sticky=tk.W + tk.E)

    def display_search_results(results, selected_option):
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        if results:
            for emp in results:
                result_text.insert(tk.END, f"Employee ID: {emp['uid']}\n")

                if selected_option == "All":
                    result_text.insert(tk.END, f"Name: {emp['name']}\n")
                    result_text.insert(tk.END, f"Position: {emp['position']}\n")
                    result_text.insert(tk.END, f"SSN: {emp['ssn']}\n")
                    result_text.insert(tk.END, f"Address: {emp['address']}\n")
                    result_text.insert(tk.END, f"Email: {emp['email']}\n")
                    result_text.insert(tk.END, f"Phone Number: {emp['phonenumber']}\n")
                    result_text.insert(tk.END, f"Skills: {emp['skills']}\n")

                elif selected_option == "Name":
                    result_text.insert(tk.END, f"Name: {emp['name']}\n")
                elif selected_option == "Address":
                    result_text.insert(tk.END, f"Address: {emp['address']}\n")
                elif selected_option == "SSN":
                    result_text.insert(tk.END, f"SSN: {emp['ssn']}\n")
                elif selected_option == "Email":
                    result_text.insert(tk.END, f"Email: {emp['email']}\n")
                elif selected_option == "Skills":
                    result_text.insert(tk.END, f"Skills: {emp['skills']}\n")
                elif selected_option == "Phone Number":
                    result_text.insert(tk.END, f"Phone Number: {emp['phonenumber']}\n")
                elif selected_option == "Position":
                    result_text.insert(tk.END, f"Position: {emp['position']}\n")

                result_text.insert(tk.END, "\n")
        else:
            result_text.insert(tk.END, "No results found.")

    result_text.config(state=tk.DISABLED)


    #empty text
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)

    return

# EULA agreement and main done by Drew Penn
"""
the check_agreement function checks to see if the user has agreed to the EULA,
which would be written as yes or no in the eula.txt. If no, creates a message box
asking them to agree, if they do they proceed to use the app, if not the app closes.
"""
def check_agreement():
    if os.path.exists(EULA_VERIFICATION):
        with open(EULA_VERIFICATION, "r") as file:
            content = file.read().strip().lower()
            if content in ["yes", "true"]:
                return True
    
    # If the user hasn't agreed before, show the eula agreement
    with open(EULA_AGREEMENT_TEXT, "r") as file:
        tos_content = file.read()
    
    agreement_root = tk.Tk()
    agreement_root.protocol("WM_DELETE_WINDOW", sys.exit)

    text_area = Text(agreement_root, wrap=tk.WORD, width=50, height=20)
    text_area.insert(tk.END, tos_content)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10)

    def on_yes():
        with open(EULA_VERIFICATION, "w") as file:
            file.write("yes")
        agreement_root.destroy()
        main()

    def on_no():
        with open(EULA_VERIFICATION, "w") as file:
            file.write("no")
        sys.exit()

    btn_yes = tk.Button(agreement_root, text="Yes, I agree", command=on_yes)
    btn_no = tk.Button(agreement_root, text="No, I don't agree", command=on_no)
    btn_yes.pack(side=tk.LEFT, padx=5, pady=10)
    btn_no.pack(side=tk.RIGHT, padx=5, pady=10)

    agreement_root.mainloop()


def main():
    if not check_agreement():
        return
    
    root = create_main_window()
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    # Main frame with grey background
    main_frame = tk.Frame(root, bg="grey")
    main_frame.pack(fill=tk.BOTH, expand=True)

    button_frame = tk.Frame(main_frame, bg="grey")
    button_frame.pack(pady=1)

    panel = tk.LabelFrame(main_frame, text="Panel", relief="sunken")
    panel.pack(fill=tk.BOTH, expand=True)

    buttons = create_buttons(button_frame, panel)
    
    # Set default panel to the first button
    create_panel_for_button(0, panel)

    root.mainloop()


if __name__ == "__main__":
    main()