from tkinter import *
from tkinter import messagebox, ttk, Text, font
from tkcalendar import Calendar, DateEntry
import submission as sub


root = Tk()
root.title('KKLJ Property Management Software BETA')
root.geometry('1000x1000')

# define a universal style for Combobox widget
style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', font=('Nexa', '11'), background='white')
root.option_add('*TCombobox*Listbox.font', ('Nexa', '11'))
style.configure('TLabel', font='Nexa 11')
style.configure('TEntry', font='Arial 11')
style.configure('TRadiobutton', font='Arial 11')
style.configure('TCheckbutton', font='Nexa 11')
style.configure('TButton', font='San_Francisco 10', background='white')


#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
'''MAIN FRAME'''
# create first frame of Stay Window
frame_main = LabelFrame(root, padx=30, pady=30, bd=5, font='Arial')
frame_main.grid(row=0, column=0, padx=30, pady=30, sticky=N)
# create title label of frame_main
global title_main
title_main = Label(frame_main, text='Booking Information',
                font='Helvetica 16 bold')
title_main.grid(row=0, columnspan=2, padx=25, pady=20, sticky=N)

# function to change property selection again
def change_back():

    property.grid_remove()
    change_again.grid_remove()
    title_main.grid(row=0, columnspan=2, padx=25, pady=20, sticky=N)
    properties_label.grid(row=1, column=0, sticky=W, padx=20, pady=10)
    property_selected.set('Select from...')
    properties_field.grid(row=1, column=1, padx=20, pady=0, sticky=E)

# function to change property headline once selected
def change_appearance(var):

    if property_selected.get() != 'Select from...':
        title_main.grid_remove()
        properties_label.grid_remove()
        properties_field.grid_remove()
        global property
        property = Label(frame_main, text=property_selected.get(),
                    font='Helvetica 16 bold')
        property.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky=N)

        # give button option to change property again if wrong selection
        global change_again
        change_again = Button(frame_main, text='Change Property',
                        command=change_back, bg='#eeeeee', font='San_Fancisco 10')
        change_again.grid(row=1, column=0, columnspan=2,
                        padx=20, pady=7, sticky=N)


# create label and field for Property
global properties_label
properties_label = ttk.Label(frame_main, text='Property')
properties_label.grid(row=1, column=0, sticky=W, padx=20, pady=10)
# create temporary properties list
properties_list = [
        'Quinta da Barracuda - A02',
        'Quinta da Barracuda - A03',
        'Quinta da Barracuda - A12',
        'Quinta da Barracuda - A13'
]
# declare StringVar for property selected
global property_selected
property_selected = StringVar()
property_selected.set('Select from...')
global properties_field
properties_field = ttk.OptionMenu(frame_main, property_selected, *properties_list,
        command=change_appearance)
propertis_field['borderwidth'] = 20
properties_field.config(width=12, font='Arial 11', anchor=W, bg='white',
                    highlightbackground='red')
properties_field.grid(row=1, column=1, padx=20, pady=0)

# create radio button for owner
owner_label = ttk.Label(frame_main, text='Owner')
owner_label.grid(row=2, column=0, sticky=W, padx=20, pady=10)
owner_selection = StringVar()
owner_selection.set('n')
owner_yes = ttk.Radiobutton(frame_main, text='Yes', value='y',
                variable=owner_selection)
owner_yes.grid(row=2, column=1, padx=25, sticky=W)
owner_no = ttk.Radiobutton(frame_main, text='No', value='n',
                variable=owner_selection)
owner_no.grid(row=2, column=1, padx=25, sticky=E)

# create name entry field for guest
guest_label = ttk.Label(frame_main, text='Guest')
guest_label.grid(row=3, column=0, sticky=W, padx=20, pady=10)
guest_name = Text(frame_main, width=16, height=1, font='Arial 11')
guest_name.grid(row=3, column=1, padx=20)

# create email entry field for guest
guest_email_label = ttk.Label(frame_main, text='Email')
guest_email_label.grid(row=4, column=0, sticky=W, padx=20, pady=10)
guest_email = Text(frame_main, width=16, height=1, font='Arial 11')
guest_email.grid(row=4, column=1, padx=20)

# create frame for party composition fields
party_frame = LabelFrame(frame_main, padx=0, pady=0, bd=0)
party_frame.grid(row=5, padx=20, column=0, columnspan=2, pady=10, sticky=W)
adult_label = ttk.Label(party_frame, text='Adults ')
adult_label.pack(side=LEFT)
adult_field = Text(party_frame, width=1, height=1, font='Arial 11', bg='light grey')
adult_field.insert(1.0, '2')
adult_field.pack(side=LEFT)
dummy_label1 = ttk.Label(party_frame, text='     ')
dummy_label1.pack(side=LEFT)
child_label = ttk.Label(party_frame, text='Children ')
child_label.pack(side=LEFT)
child_field = Text(party_frame, width=1, height=1, font='Arial 11', bg='light grey')
child_field.pack(side=LEFT)
dummy_label2 = ttk.Label(party_frame, text='      ')
dummy_label2.pack(side=LEFT)
baby_label = ttk.Label(party_frame, text='Babies ')
baby_label.pack(side=LEFT)
baby_field = Text(party_frame, width=1, height=1, font='Arial 11', bg='light grey')
baby_field.pack(side=LEFT)

# declare string variables for dates
arrival_str = StringVar()
departure_str = StringVar()

# labels for the calendar inputs
arrival_label = ttk.Label(frame_main, text='Arriving')
arrival_label.grid(row=6, column=0, sticky=W, padx=20, pady=10)
departure_label = ttk.Label(frame_main, text='Departing')
departure_label.grid(row=7, column=0, sticky=W, padx=20, pady=10)
# initialise and place arrival and departure calendars
arrival_cal = DateEntry(frame_main, textvariable=arrival_str,
        selectmode='day', locale='en_UK', font='Arial 11',
        showweeknumbers=False, showothermonthdays=False,
        weekendbackground='#ededed', weekendforeground='black',
        width=14)
departure_cal = DateEntry(frame_main, textvariable=departure_str,
        selectmode='day', locale='en_UK', font='Arial 11',
        showweeknumbers=False, showothermonthdays=False,
        weekendbackground='#ededed', weekendforeground='black',
        width=14)
arrival_cal.grid(row=6, column=1)
departure_cal.grid(row=7, column=1)

# function to display according to transport method selcted
def transport_option(var):

    if transport_selected.get() == 'Flight':
        flight_window = Toplevel()
        flight_window.title('Enter Guest Flight Details')
        global inbound_no
        global inbound_time
        global outbound_no
        global outbound_time
        flight_no = ttk.Label(flight_window, text='Flight Nº')
        flight_no.grid(row=0, column=1, sticky=W, padx=20, pady=10)
        flight_time = ttk.Label(flight_window, text='Time')
        flight_time.grid(row=0, column=2, sticky=W, padx=20, pady=10)
        inbound = ttk.Label(flight_window, text='Inbound')
        inbound.grid(row=1, column=0, sticky=W, padx=20, pady=10)
        inbound_no = Text(flight_window, width=10, height=1, font='Arial 11')
        inbound_no.grid(row=1, column=1, padx=20)
        inbound_time = Text(flight_window, width=7, height=1, font='Arial 11')
        inbound_time.grid(row=1, column=2, padx=20)
        outbound = ttk.Label(flight_window, text='Outbound')
        outbound.grid(row=2, column=0, sticky=W, padx=20, pady=10)
        outbound_no = Text(flight_window, width=10, height=1, font='Arial 11')
        outbound_no.grid(row=2, column=1, padx=20)
        outbound_time = Text(flight_window, width=7, height=1, font='Arial 11')
        outbound_time.grid(row=2, column=2, padx=20)

        save_button = ttk.Button(flight_window, text='Save',
            command=flight_window.destroy)
        save_button.grid(row=3, column=1, padx=20, pady=20)


# create a check for mode of transportation
transport_label = ttk.Label(frame_main, text='Transportation')
transport_label.grid(row=9, column=0, sticky=W, padx=20, pady=10)
transport_options = [
        'Flight',
        'Car',
        'Train',
        'Bus'
        ]
transport_selected = StringVar()
transport_selected.set('Coming by...')
transport_field = OptionMenu(frame_main, transport_selected,
                        *transport_options, command=transport_option)
transport_field.config(width=12, font='Arial 11', anchor=W)
transport_field.grid(row=9, column=1, padx=20, pady=0)

# create radio button for car hire
carhire_label = ttk.Label(frame_main, text='Hiring a Car')
carhire_label.grid(row=10, column=0, sticky=W, padx=20, pady=10)
carhire_selection = StringVar()
carhire_selection.set('n')
carhire_yes = ttk.Radiobutton(frame_main, text='Yes', value='y',
                variable=carhire_selection)
carhire_yes.grid(row=10, column=1, padx=25, sticky=W)
carhire_no = ttk.Radiobutton(frame_main, text='No', value='n',
                variable=carhire_selection)
carhire_no.grid(row=10, column=1, padx=25, sticky=E)

# create dropdown for hours and mins for ETA declaration
eta_label = ttk.Label(frame_main, text='ETA')
eta_label.grid(row=12, column=0, sticky=W, padx=20, pady=10)
hrs_selected = StringVar()
mins_selected = StringVar()
eta_hrs = ttk.Combobox(frame_main, textvariable=hrs_selected,
                state='readonly', width=4, font='Arial 11')
eta_hrs['values'] = ['HH', '00', '01', '02', '03', '04', '05', '06', '07', '08',
                    '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                    '19', '20', '21', '22', '23']
eta_hrs.set('HH')
eta_hrs.grid(row=12, column=1, padx=26, sticky=W)
eta_mins = ttk.Combobox(frame_main, textvariable=mins_selected,
                state='readonly', width=4, font='Arial 11')
eta_mins['values'] = ['MM', '00', '15', '30', '45']
eta_mins.set('MM')
eta_mins.grid(row=12, column=1, padx=26, sticky=E)



#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
"""FRAME TO CONTAIN SERVICES AND EXTRAS FRAMES"""

container2 = LabelFrame(root, bd=0)
container2.grid(row=0, column=1, padx=0, pady=25, sticky=N)


#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
"""EXTRAS FRAME"""

# create second frame of Stay Window
frame_extras = LabelFrame(container2, padx=23, pady=30, bd=5)
frame_extras.grid(row=1, column=0, padx=0, pady=20, sticky=N)
# create title label of frame_main
title_extras = Label(frame_extras, text='Extras for Guest',
                font='Helvetica 16 bold')
title_extras.grid(row=0, padx=20, pady=20, columnspan=2, sticky=N)

# create labels and checkboxes for extras
at_var = StringVar()
airport_transfer = ttk.Checkbutton(frame_extras, text='Airport Transfer',
                    variable=at_var, onvalue='y', offvalue='n')
airport_transfer.grid(row=1, column=0, padx=20, pady=5, sticky=W)

wp_var = StringVar()
welcome_pack = ttk.Checkbutton(frame_extras, text='Welcome Pack',
                    variable=wp_var, onvalue='y', offvalue='n')
welcome_pack.grid(row=4, column=0, padx=20, pady=5, sticky=W)

cot_var = StringVar()
cot = ttk.Checkbutton(frame_extras, text='Cot',
                    variable=cot_var, onvalue='y', offvalue='n')
cot.grid(row=4, column=1, padx=20, pady=5, sticky=W)

hc_var = StringVar()
high_chair = ttk.Checkbutton(frame_extras, text='High Chair',
                    variable=hc_var, onvalue='y', offvalue='n')
high_chair.grid(row=1, column=1, padx=20, pady=5, sticky=W)



#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
"""MANAGEMENT FRAME"""
# create third frame of Stay Window
frame_clean = LabelFrame(container2, padx=25, pady=30, bd=5)
frame_clean.grid(row=0, column=0, padx=0, pady=5, sticky=N)
# create title for the cleaning frame
title_clean = Label(frame_clean, text='Management Services',
                font='Helvetica 16 bold')
title_clean.grid(row=0, padx=40, pady=20, columnspan=2, sticky=N)

# create function to save other clean descriptions
def save_descriptions():

    global oc_description
    global oc_charge
    oc_description = description_box.get(1.0, 'end-1c')
    oc_charge = charge_box.get(1.0, 'end-1c')
    oc_window.destroy()


# create function to accept details of other type of clean
def other_clean():

    if c_selection.get() == 'o':
        # create other clean frame
        global oc_window
        oc_window = Toplevel()
        oc_window.title('Specify Other Type')
        global description_box
        global charge_box
        description_label = ttk.Label(oc_window, text='Describe Clean',
                                font='Nato 11')
        description_label.grid(row=0, column=0, padx=20, pady=10, sticky=W)
        description_box = Text(oc_window, width=17, height=1, font='Arial 10')
        description_box.grid(row=1, column=0, padx=20, sticky=W)
        charge_label = ttk.Label(oc_window, text='Charge (€)',
                            font='Nato 11')
        charge_label.grid(row=0, column=1, padx=20, pady=10, sticky=W)
        charge_box = Text(oc_window, width=8, height=1, font='Arial 10')
        charge_box.grid(row=1, column=1, columnspan=2, padx=20, sticky=W)

        save_button = ttk.Button(oc_window, text='Save',
            command=save_descriptions)
        save_button.grid(row=3, columnspan=2, padx=20, pady=20)

# create cleaning options
c_selection = StringVar()
c_selection.set('y')
cleaning_label = Label(frame_clean, text='Clean Type', font='Nexa 12 bold')
cleaning_label.grid(row=2, column=0, columnspan=2, padx=50, pady=20, sticky=W)
# create frame to stack cleaning options
ctypes_frame = LabelFrame(frame_clean, padx=0, pady=10, bd=0)
ctypes_frame.grid(row=2, column=1, padx=30, pady=3, sticky=E)
c_yes = Radiobutton(ctypes_frame, text='Full Clean', value='y',
                variable=c_selection, command=other_clean, font='Arial 11')
c_yes.grid(row=0, column=0, padx=0,pady=5, sticky=W)
c_no = Radiobutton(ctypes_frame, text='No Clean', value='n',
                variable=c_selection, command=other_clean, font='Arial 11')
c_no.grid(row=1, column=0, padx=0, pady=5, sticky=W)
c_other = Radiobutton(ctypes_frame, text='Other Type', value='o',
                variable=c_selection, command=other_clean, font='Arial 11')
c_other.grid(row=2, column=0, padx=0, pady=5, sticky=W)

# make gap between two services
Label(frame_clean, text='').grid(row=5)

# create radio button for meet & greet
mg_selection = StringVar()
mg_selection.set('y')
cleaning_label = Label(frame_clean, text='Meet & Greet', font='Nexa 12 bold')
cleaning_label.grid(row=6, column=0, columnspan=2, padx=28, pady=10, sticky=W)
mg_yes = Radiobutton(frame_clean, text='Yes', value='y',
                variable=mg_selection, font='Arial 11')
mg_yes.grid(row=6, column=1, padx=77, pady=5, ipadx=0, sticky=E)
mg_no = Radiobutton(frame_clean, text='No', value='n',
                variable=mg_selection, font='Arial 11')
mg_no.grid(row=6, column=1, padx=20, pady=5, sticky=E)



#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
"""CHECKS AND SUBMISSION"""
# triggered when value of string variable changes
def check_submission():
    """
    # read and check if dates are valid, and confirm the string content of name
    # and email
    if int(arrival_str.get()[-4:]) > int(departure_str.get()[-4:]):
        messagebox.showerror('Invalid Dates', 'Arrival is after Departure')
        return

    elif (int(arrival_str.get()[-4:]) == int(departure_str.get()[-4:])
        and int(arrival_str.get()[3:5]) > int(departure_str.get()[3:5])):
        messagebox.showerror('Invalid Dates', 'Arrival is after Departure')
        return

    elif (int(arrival_str.get()[-4:]) == int(departure_str.get()[-4:])
        and int(arrival_str.get()[3:5]) == int(departure_str.get()[3:5])
        and int(arrival_str.get()[0:2]) > int(departure_str.get()[0:2])):
        messagebox.showerror('Invalid Dates', 'Arrival is after Departure')
        return

    elif (int(arrival_str.get()[-4:]) == int(departure_str.get()[-4:])
        and int(arrival_str.get()[3:5]) == int(departure_str.get()[3:5])
        and int(arrival_str.get()[0:2])== int(departure_str.get()[0:2])):
        messagebox.showerror('Invalid Dates', 'Arrival is same as Departure')
        return

    elif guest_name.get(1.0, 'end-1c') == '':
        response = messagebox.askokcancel('No Guest',
                    'Guest name field is empty. Continue anyway?')
        if response == 1:
            pass
        else:
            return
    elif guest_email.get(1.0, 'end-1c') == '':
        response = messagebox.askokcancel('No Email',
                    'Guest email field is empty. Continue anyway?')
        if response == 1:
            pass
        else:
            return
    elif adult_field.get(1.0, 'end-1c') == '':
        response = messagebox.askokcancel('No Adults',
                    'Adult field is empty. Continue anyway?')
        if response == 1:
            pass
        else:
            return
    else:
        submit.grid_remove()
    """
    submit.grid_remove()
    #<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
    #<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
    """CHARGES FRAME"""
    # create charges frame after first submission
    frame_charges = LabelFrame(root, padx=10, pady=20, bd=5)
    frame_charges.grid(row=1, column=0, columnspan=2, padx=30, pady=0, sticky=N)
    ocharges_title = Label(frame_charges, text='Charges to Owner',
                        font='Helvetica 14 bold')
    ocharges_title.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky=N)
    gcharges_title = Label(frame_charges, text='Charges to Guest',
                        font='Helvetica 14 bold')
    gcharges_title.grid(row=0, column=3, columnspan=3, padx=20, pady=20, sticky=N)

    # create charges header labels
    type_charge_label = ttk.Label(frame_charges, text='Charge', font='Lato 13')
    type_charge_label.grid(row=1, column=0, padx=5, pady=0, sticky=E)
    cost_charge_label = ttk.Label(frame_charges, text='Cost (€)', font='Lato 13')
    cost_charge_label.grid(row=1, column=1, padx=0, pady=0)
    description_charge_label = ttk.Label(frame_charges, text='Description',
                                    font='Lato 13')
    description_charge_label.grid(row=1, column=2, padx=5, pady=0, sticky=W)

    header_separator = ttk.Separator(frame_charges, orient='horizontal')
    header_separator.grid(row=2, column=0, columnspan=3, padx=10,
                        pady=0, ipadx=180)

    # create owner charges breakdown
    # create clean charge submission
    charge_clean_label = ttk.Label(frame_charges, text='Cleaning',
                            font='Tlwg_Typist 12')
    charge_clean_label.grid(row=3, column=0, padx=10, pady=10, sticky=E)
    charge_clean_box = Text(frame_charges, width=7, height=1, font='Arial 11')
    charge_clean_box.grid(row=3, column=1, padx=10, pady=10)
    # produce description for the charge description
    if c_selection.get() == 'y':
        desc = 'Full Clean'
    elif c_selection.get() == 'n':
        desc = 'No Clean'
    else:
        desc = 'Other: ' + oc_description
    charge_clean_description = ttk.Label(frame_charges, text=desc,
                                    font='Tlwg_Typist 10 italic')
    charge_clean_description.grid(row=3, column=2, padx=10, pady=10, sticky=W)



# button to submit initial details and perform checks
submit = Button(root, text='Generate Charges', command=check_submission,
            font='San_Francisco 14', background='white')
submit.grid(row=1, column=0, columnspan=2, padx=20, pady=30, ipadx=40, sticky=S)

date = Label(root, text='')
date.grid(row=7, column=0, columnspan=2)



root.mainloop()
