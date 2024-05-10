from tkinter import *

class PlaceholderEntry(Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = "grey"
        self.default_color = self["fg"]
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.insert(0, self.placeholder)  # Insert the placeholder initially
        self["fg"] = self.placeholder_color  # Set placeholder color initially

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, END)
            self["fg"] = self.default_color

    def on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color


def showTask():
    try:
        with open('data.txt','r') as file:
            tasks = file.readlines()
            tasks = [_.strip() for _ in tasks]
    except:
        with open('data.txt', 'w') as file:
            tasks = []

    table.delete(0,'end')    

    for task in tasks:
        table.insert('end', task)


def addTask():
    task = search_entry.get()
    if task != "Enter task here":
        with open('data.txt','a') as file:
            file.write(f"{task}\n")
    search_entry.delete(0,'end')
    showTask()

def deleteTask():

    with open('data.txt','r') as file:
        tasks=file.readlines()
        tasks=[_.strip() for _ in tasks]    

    tasks.remove(selected_task)
    with open('data.txt','w') as file:
        for task in tasks:
            file.write(f"{task}\n")
    showTask()

selected_task = ''
def onTaskSelect(event):
    global selected_task 
    # Get the selected index
    selected_index = table.curselection()
    if selected_index:
        # Get the value at the selected index
        selected_task = table.get(selected_index)
    else:
        selected_task = ''

def updateTask():
    def updateOk():
        new_task = entry.get()
        with open("data.txt", 'r') as file:
            tasks=file.readlines()
            tasks=[_.strip() for _ in tasks]  

        tasks[table.curselection()[0]] = new_task
        with open('data.txt', 'w') as file:
            for task in tasks:
                file.write(f"{task}\n")      
        showTask()
        update_window.destroy()

    update_window = Tk()
    update_window_frame = Frame(update_window)
    update_window_frame.pack(padx=10, pady=10)
    update_window.title('Update Task')
    update_window.minsize(width=100, height=100)

    if selected_task!="":
        previous_task = Label(update_window_frame, text=f"Task : {selected_task}", font=('Arial',20))
        previous_task.pack(padx=10, pady=10)

        entry = PlaceholderEntry(update_window_frame, width=20, font=('Arial',18),placeholder="Update the task")
        entry.pack(padx=10, pady=10)

        button = Button(update_window_frame,text="Ok", font=('Arial',20), command=updateOk)
        button.pack(padx=10, pady=10)
    else :
        def ok():
            update_window.destroy()
        label_ = Label(update_window_frame, text="Please select a task.", font=('Arial',20))
        label_.pack(padx=10, pady=10)

        button_ = Button(update_window_frame, text='Ok', font=('Arial,20'), command=ok)
        button_.pack(padx=10, pady=10)

    mainloop()

def exitApp():
    root.destroy()


root = Tk()

frame = Frame(root)
frame.pack()

root.minsize(width=400, height=600)
root.title("TO-DO LIST")

frame1 = Frame(frame)
frame1.pack()

frame2 = Frame(frame)
frame2.pack()

frame3 = Frame(frame2)
frame3.grid(row=0, column=0)

frame4 = Frame(frame2)
frame4.grid(row=0, column=1, padx=10)

to_do_list_label = Label(frame1, text='To-Do List', font=('Arial',20,'bold'),height=2, width=8)
to_do_list_label.pack()

add_btn = Button(frame3, text='Add', font=('Arial',15),height=2, width=8, command=addTask)
add_btn.pack()

update_btn = Button(frame3, text='Update', font=('Arial',15),height=2, width=8, command=updateTask)
update_btn.pack()

delete_btn = Button(frame3, text='Delete', font=('Arial',15),height=2, width=8, command=deleteTask)
delete_btn.pack()

exit_btn = Button(frame3, text='Exit', font=('Arial',15),height=2, width=8, command=exitApp)
exit_btn.pack()

search_entry = PlaceholderEntry(frame4, width=40, font=('Arial',18),placeholder="Enter task here")
search_entry.pack(pady=10)

scrollbar = Scrollbar(frame4, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

table = Listbox(frame4, font=('Arial', 12), height=10, width=87, yscrollcommand=scrollbar.set)
table.pack()

scrollbar.config(command=table.yview)

showTask()

# Bind the callback function to mouse click event on the Listbox
table.bind('<<ListboxSelect>>', onTaskSelect)

root.mainloop()



