from tkinter import *
import csv
from tkinter import messagebox

phonebook = []
def ReadCSVFile():
	global header
	with open('database.csv') as csvfile:
		csv_reader = csv.reader(csvfile,delimiter=',')
		header = next(csv_reader)
		for row in csv_reader:
			phonebook.append(row)
	set_select()		
	print(phonebook)


def WriteInCSVFile(phonebook):
	with open('database.csv','w',newline='') as csv_file:
		writeobj = csv.writer(csv_file,delimiter=',')
		writeobj.writerow(header)
		for row in phonebook:
			writeobj.writerow(row)

def WhichSelected():
	print("hello",len(select.curselection()))
	if len(select.curselection())==0:
		messagebox.showerror("Error", "Please Select the Name")
	else:
		return int(select.curselection()[0])
		
def set_select():
    phonebook.sort(key=lambda record: record[0])
    select.delete(0, END)
    i=0
    for name, phone in phonebook:
    	i+=1
    	select.insert(END, f"{i}  |    {name}   |   {phone}")

def AddDetail():
	if E_name.get()!="" and E_last_name.get()!="" and E_contact.get()!="":
		phonebook.append([E_name.get()+' '+E_last_name.get(),E_contact.get()])
		print(phonebook)
		WriteInCSVFile(phonebook)
		set_select()
		EntryReset()
		messagebox.showinfo("Confirmation", "Succesfully Add New Contact")
		
	else:
		messagebox.showerror("Error", "Please fill the information")


def UpdateDetail():
	if E_name.get() and E_last_name.get() and E_contact.get():
		phonebook[WhichSelected()] = [ E_name.get()+' '+E_last_name.get(), E_contact.get()]
		WriteInCSVFile(phonebook)
		messagebox.showinfo("Confirmation", "Succesfully Update Contact")
		EntryReset()
		set_select()

	elif not(E_name.get()) and not(E_last_name.get()) and not(E_contact.get()) and not(len(select.curselection())==0):
		messagebox.showerror("Error", "Please fill the information")

	else:
		if len(select.curselection())==0:
			messagebox.showerror("Error", "Please Select the Name and \n press Load button")
		else:
			message1 = """To Load the all information of \n 
						  selected row press Load button\n.
						  """
			messagebox.showerror("Error", message1)

def EntryReset():
	E_name_var.set('')
	E_last_name_var.set('')
	E_contact_var.set('')

def DeleteEntry():
	if len(select.curselection())!=0:
		result=messagebox.askyesno('Confirmation','You Want to Delete Contact\n Which you selected')
		if result==True:
			del phonebook[WhichSelected()]
			WriteInCSVFile(phonebook)
			set_select()
	else:
		messagebox.showerror("Error", 'Please select the Contact')


def LoadEntry():
    name, phone = phonebook[WhichSelected()]
    print(name.split(' '))
    E_name_var.set(name.split()[0])
    E_last_name_var.set(name.split()[1])
    E_contact_var.set(phone)


def binary_search(phonebook, target_name):
    left = 0
    right = len(phonebook) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_name = phonebook[mid][0].split()[0]


        if mid_name == target_name:
            return phonebook[mid][1]
        elif mid_name < target_name:
            left = mid + 1
        else:
            right = mid - 1

    return None

def search_name():
    name_to_search = str(s_search_var.get())
    result = binary_search(phonebook, name_to_search)

    if result:
        messagebox.showinfo("Result", f"{name_to_search}'s phone number is {result}")
    else:
        messagebox.showerror("Result", f"{name_to_search} not found in the phonebook")

def call():
	name_to_search = s_search_var.get()
	result = binary_search(phonebook, name_to_search)
	
	if result:
		messagebox.showinfo("Calling ", f"{name_to_search}, {result}...........")
	else:
		messagebox.showinfo("Error ", f"{name_to_search}, {result} ")

def message():
	name_to_search = s_search_var.get()
	result = binary_search(phonebook, name_to_search)
	
	if result:
		messagebox.showinfo("Messaging ", f"{name_to_search}, {result} ...........")
	else:
		messagebox.showinfo("Error ", f"{name_to_search}, {result} ")

window = Tk()

Frame1 = LabelFrame(window,text="Enter the Contact Detail")
Frame1.grid(padx=15,pady=15)


Inside_Frame1 = Frame(Frame1)
Inside_Frame1.grid(row=0,column=0,padx=15,pady=15)

l_name = Label(Inside_Frame1,text="Name")
l_name.grid(row=0,column=0,padx=5,pady=5)
E_name_var = StringVar()

E_name = Entry(Inside_Frame1,width=30, textvariable=E_name_var)
E_name.grid(row=0,column=1,padx=5,pady=5)

l_last_name= Label(Inside_Frame1,text="Last Name")
l_last_name.grid(row=1,column=0,padx=5,pady=5)
E_last_name_var= StringVar()
E_last_name = Entry(Inside_Frame1,width=30,textvariable=E_last_name_var)
E_last_name.grid(row=1,column=1,padx=5,pady=5)

l_contact= Label(Inside_Frame1,text="Number")
l_contact.grid(row=2,column=0,padx=5,pady=5)
E_contact_var = StringVar()
E_contact = Entry(Inside_Frame1,width=30,textvariable=E_contact_var)
E_contact.grid(row=2,column=1,padx=5,pady=5)

Frame2 = Frame(window)
Frame2.grid(row=0,column=1,padx=15,pady=15,sticky=E)

Add_button = Button(Frame2,text="Add Detail",width=15,bg="#6B69D6",fg="#FFFFFF",command=AddDetail)
Add_button.grid(row=0,column=0,padx=8,pady=8)

Update_button = Button(Frame2,text="Update Detail",width=15,bg="#6B69D6",fg="#FFFFFF",command=UpdateDetail)
Update_button.grid(row=1,column=0,padx=8,pady=8)


Reset_button = Button(Frame2,text="Reset",width=15,bg="#6B69D6",fg="#FFFFFF",command=EntryReset)
Reset_button.grid(row=2,column=0,padx=8,pady=8)

Load_button = Button(Frame2,text="Load",width=15,bg="#6B69D6",fg="#FFFFFF",command=LoadEntry)
Load_button.grid(row=3,column=0,padx=8,pady=8)


Frame3 = LabelFrame(window,text="Enter the name to search")
Frame3.grid(row=2,column=0,padx=15,pady=15)

Inside_Frame3 = Frame(Frame3)
Inside_Frame3.grid(row=0,column=0,padx=15,pady=15)
s_search= Label(Inside_Frame3,text="Search ")
s_search.grid(row=0,column=0,padx=5,pady=5)
s_search_var = StringVar()
s_search = Entry(Inside_Frame3,width=30, textvariable=s_search_var)
s_search.grid(row=0,column=1,padx=5,pady=5)


call_button = Button(Inside_Frame3,text="Call",width=15,bg="#6B69D6",fg="#FFFFFF", command=call)
call_button.grid(row=1,column=0,padx=5,pady=5)

message_button = Button(Inside_Frame3,text="Message",width=15,bg="#6B69D6",fg="#FFFFFF", command=message)
message_button.grid(row=1,column=1,padx=5,pady=5)

Frame4 = Frame(window)
Frame4.grid(row=2,column=1,padx=15,pady=15,sticky=E)

search_button = Button(Frame4,text="Search",width=15,bg="#6B69D6",fg="#FFFFFF",command=search_name)
search_button.grid(row=0,column=3,padx=5,pady=5)

Delete_button = Button(Frame4,text="Delete",width=15,bg="#D20000",fg="#FFFFFF",command=DeleteEntry)
Delete_button.grid(row=1,column=3,padx=5,pady=5,sticky=S)


DisplayFrame = Frame(window)
DisplayFrame.grid(row=1,column=0,padx=15,pady=15)

scroll = Scrollbar(DisplayFrame, orient=VERTICAL)
select = Listbox(DisplayFrame, yscrollcommand=scroll.set,font=("Arial Bold",10),bg="#282923",fg="#E7C855",width=40,height=10,borderwidth=3,relief="groove")
scroll.config(command=select.yview)
select.grid(row=0,column=0,sticky=W)
scroll.grid(row=0,column=1,sticky=N+S)


ReadCSVFile()

window.mainloop()
