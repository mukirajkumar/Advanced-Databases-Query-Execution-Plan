import threading
from tkinter import *
from preprocessing import *
from annotation import *

class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# (Main) Database login page
def login_window():
    global login_window
    login_window = Tk()
    login_window.title("Database Login")
    login_window.geometry('380x430')
    login_window.config(bg='white')

# Variables for the username, password and database inputs
    global username_input
    global password_input
    global db_input

# Variables for the verification of the username, password and database inputs
    global username_ver
    global password_ver
    global db_ver

    global count
    username_ver = StringVar()
    password_ver = StringVar()
    db_ver = StringVar()

    Label(login_window, text="Please input the following details to login to the database:", wraplength='300', height='2', bg = 'white', font=('Open Sans', 14)).pack(ipadx=10, ipady=10)
    Label(login_window, text="Username", width='10', bg = 'white', height='2', font=('Open Sans', 14)).pack()
    username_input = Entry(login_window, textvariable=username_ver).pack()

    Label(login_window, text="Password", width='10',bg = 'white', height='2', font=('Open Sans', 14)).pack()
    password_input = Entry(login_window, textvariable=password_ver, show='*').pack()

    Label(login_window, text="Database Name", width='15', bg = 'white', height='2', font=('Open Sans', 14)).pack()
    db_input = Entry(login_window, textvariable=db_ver).pack()

    Label(login_window, text="Note: Input is case-sensitive", width='100', bg = 'white', height='2', font=('Open Sans', 14)).pack()
    HoverButton(login_window, text="Login", width='15', height='1', font=('Open Sans', 14), fg="white", bg = '#024d23', activebackground = '#04c256', command=login_success).pack()

    login_window.mainloop()

fail_label = None

# Correct login details - grants access to the SQL GUI
# Incorrect login details - text to indicate this appears
def login_success():
    username1 = username_ver.get()
    password1 = password_ver.get()
    db1 = db_ver.get()
    result = authenticate_connect(username1, password1, db1)
    if result:
        dbgui()
    else:
        global fail_label
        if not fail_label:
            fail_label = Label(login_window, text="Incorrect login details, please try again!", wraplength='400',font=('Open Sans', 14), fg='red', bg ='white', height='2')
            fail_label.pack()


# Submit function for query
def submit_query():
    query = user_query.get('1.0', 'end-1c')
    qep_panel_text.configure(state='normal')
    qep_panel_text.delete('1.0', 'end-1c')
    # Nothing submitted:
    if not query:
        qep_panel_text.insert(END, "Empty submission, please submit an SQL query\n")
        qep_panel_text.config(fg='red')
        qep_panel_text.configure(state='disabled')

    # Recognisable query - annotation generated based on user's query:
    else:
        x = runQuery(query)
        # Unrecognisable query - annotation cannot be generated:
        if not x:
            qep_panel_text.config(fg='red')
            qep_panel_text.insert(END, "Please check your SQL query")
            qep_panel_text.configure(state='disabled')
        else:
            annotated_query = startAnnotation()
            qep_panel_text.config(fg='black')
            qep_panel_text.insert(END,annotated_query[3])
        qep_panel_text.configure(state='disabled')



# Getting rid of windows:
# Deletion of (Main) Database login page
def del_login_window():
    login_window.destroy()
# Deletion of SQL GUI
def del_gui():
    window.destroy()


# Visualize the QEP json file into a tree structure
def viewQEPTree():
    def callback():
        createQEPTreeDiagram()
    t = threading.Thread(target=callback)
    t.start()

# Visualize the first AQP json file into a tree structure
def viewFirstAQPTree():
    def callback():
        createFirstAQPTreeDiagram()
    t = threading.Thread(target=callback)
    t.start()

# Visualize the second AQP json file into a tree structure
def viewSecondAQPTree():
    def callback():
        createSecondAQPTreeDiagram()
    t = threading.Thread(target=callback)
    t.start()

# Visualize the third AQP json file into a tree structure
def viewThirdAQPTree():
    def callback():
        createThirdAQPTreeDiagram()
    t = threading.Thread(target=callback)
    t.start()

def clearQueries():
    qep_panel_text.configure(state='normal')
    qep_panel_text.delete('1.0', 'end-1c')
    qep_panel_text.configure(state='disabled')
    user_query.delete('1.0','end-1c')
    clearAnnotation()
    if os.path.exists("actual_queryplans/altqueryplan0.json"):
        os.remove("actual_queryplans/altqueryplan0.json")
    if os.path.exists("actual_queryplans/altqueryplan1.json"):
        os.remove("actual_queryplans/altqueryplan1.json")
    if os.path.exists("actual_queryplans/altqueryplan2.json"):
        os.remove("actual_queryplans/altqueryplan2.json")
    if os.path.exists("actual_queryplans/queryplan.json"):
        os.remove("actual_queryplans/queryplan.json")


#gui for the main applicaiton
def dbgui():
    del_login_window()
    global window
    global user_query
    global qep_panel_text
    global leftPanel_text
    global centrePanel_text
    global rightPanel_text

    # Window settings
    window = Tk()
    window.geometry("700x580")
    window.title("TPC-H Database")
    window.config(bg = 'white')

    # Menubar settings
    menubar = Menu(window, background= '#04495c')
    menubar.add_command(label="Exit", font=("Open Sans", 12), command=del_gui)
    window.config(menu=menubar)


    # SQL Query Window display settings
    querypanel = PanedWindow(bg='white')
    querypanel_label = Label(querypanel, text="Input SQL Query Here", bg='white', font=("Open Sans", 14))
    querypanel_label.pack(pady=5)
    querypanel.pack()

    # SQL Query Scrollbar settings
    scrollbar = Scrollbar(querypanel)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Textbox for SQL Statement
    user_query = Text(querypanel,height=9, relief='solid', wrap='word', bg = '#d4f0fc', font=('Open Sans',10),yscrollcommand=scrollbar.set)
    user_query.pack()
    scrollbar.config(command=user_query.yview)

    # Panel for button
    div = PanedWindow(bg='white')

    # Call preprocessing.py to execute query
    submitButton = HoverButton(div, text="Submit Query", fg="white", bg = '#024d23', activebackground = '#04c256', relief=RAISED, font=("Open Sans", 12), width=15, command=submit_query)
    submitButton.pack(side=LEFT, padx=5)
    
    #call a webpage on Chrome to display the QEP
    qeptreebtn = HoverButton(div, text="View QEP Tree", fg="white", bg = '#01384a', activebackground = '#036e91', relief=RAISED, font=("Open Sans", 12), width=20,command=viewQEPTree)
    qeptreebtn.pack(side=LEFT, padx=5)

    #Clear user query
    clearbtn = HoverButton(div, text="Clear", relief=RAISED, fg="white", bg = '#5c040a', activebackground = '#c20411',font=("Open Sans", 12), width=20,
                     command=clearQueries)
    clearbtn.pack(side= LEFT, padx=5)

    div.pack(pady=5)

    # Panel for Annotated Query Plan
    annotatedPanel = PanedWindow(bg= 'white')
    annotatedPanel_label = Label(annotatedPanel, text="Annotated Query Execution Plan", bg='white', font=("Open Sans", 14) , fg = 'black')
    annotatedPanel_label.pack(pady=5)
    annotatedPanel.pack(pady=5)

    # Annotated Panel scrollbar setting
    scrollbar2 = Scrollbar(annotatedPanel)
    scrollbar2.pack(side=RIGHT, fill=Y)

    # Textbox for user to input SQL Query
    qep_panel_text = Text(annotatedPanel, state='disabled', height=14, relief='solid', wrap='word', font=('Open Sans', 10), bg = '#d4f0fc', yscrollcommand=scrollbar2.set, width = 80)
    qep_panel_text.pack()
    scrollbar2.config(command=qep_panel_text.yview)

    # Panel for button
    aqp_buttons = PanedWindow(bg='white')

    # Button to view first alternative query plan
    firstaqpButton = HoverButton(aqp_buttons, text="View First AQP Tree", fg="white", bg = '#01384a', activebackground = '#036e91', relief=RAISED, font=("Open Sans", 12), width=20, command=viewFirstAQPTree)
    firstaqpButton.pack(side=LEFT, padx=5)

    # Button to view second alternative query plan
    firstaqpButton = HoverButton(aqp_buttons, text="View Second AQP Tree", fg="white", bg = '#01384a', activebackground = '#036e91', relief=RAISED, font=("Open Sans", 12), width=20, command=viewSecondAQPTree)
    firstaqpButton.pack(side=LEFT, padx=5)

    # Button to view third alternative query plan
    firstaqpButton = HoverButton(aqp_buttons, text="View Third AQP Tree", fg="white", bg = '#01384a', activebackground = '#036e91', relief=RAISED, font=("Open Sans", 12), width=20, command=viewThirdAQPTree)
    firstaqpButton.pack(side=LEFT, padx=5)

    aqp_buttons.pack(pady=8)

    window.mainloop()





