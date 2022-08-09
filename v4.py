from tkinter import *
from tkinter import messagebox, ttk, Text, font
from tkcalendar import Calendar, DateEntry
import submission as sub
import properties as prop
import classes as cl


root = Tk()
root.title('KKLJ Property Management Software BETA')
root.geometry('1000x1000')
root.configure(bg='#efe5d9')

# create Stay Frame
stay_frame = LabelFrame(root)
stay_frame.grid(row=0, column=0)

# define a universal style for Combobox widget
style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', font=('Nexa', '11'), background='white')
root.option_add('*TCombobox*Listbox.font', ('Nexa', '11'))
style.configure('TLabel', font='Nexa 11', background='#f9f5f0')
style.configure('TEntry', font='Arial 11')
style.configure('TRadiobutton', font='Arial 11', background='#f9f5f0')
style.configure('TCheckbutton', font='Nexa 11', background='#f9f5f0')
style.configure('TButton', font='San_Francisco 10', background='white')


#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
"""FUNCTIONS"""




# universal function for save button option #
# destroys window and returns a list with necessary values
def save(id, window, lst):

    if id == 1:
        # code to store/save flight details entered into flight_window
        global flight_dict
        flight_dict = {
            'in_no': lst[0].get(1.0, 'end-1c'),
            'in_time': lst[1].get(1.0, 'end-1c'),
            'out_no': lst[2].get(1.0, 'end-1c'),
            'out_time': lst[3].get(1.0, 'end-1c')
        }
        window.destroy()

    elif id == 2:
        # code to store/save other clean description and charge of custom_window
        global other_clean_dict
        other_clean_dict = {
            'description': lst[0].get(1.0, 'end-1c'),
            'charge': lst[1].get(1.0, 'end-1c')
        }
        window.destroy()

    elif id == 3:
        # code to put description of custom owner charge in place of button
        owner_custom_button.destroy()
        ttk.Label(owner_charges,
                    text=lst[0].get(1.0, 'end-1c'),
                    **rcolumn_M_options).grid(row=5,
                                                **rcolumn_G_options)
        window.destroy()

    elif id == 4:
        # code to put description of custom guest charge in place of button
        guest_custom_button.destroy()
        custom_desc = ttk.Label(guest_charges,
                                text=lst[0].get(1.0, 'end-1c'),
                                **rcolumn_M_options).grid(row=row_count,
                                                            **rcolumn_G_options)
        window.destroy()


# function to display according to transport method selcted #
def transport_option(var):

    if transport_selected.get() == 'Flight':

        # create pop-up window to take in flight details
        flight_window = Toplevel(bg='#f9f5f0', padx=5)
        flight_window.title('Enter Guest Flight Details')

        label_G_options = {'sticky': W, 'padx': 20, 'pady': 10}
        text_M_options = {'master': flight_window, 'height': 1, 'font': 'Arial 11'}

        # head and side labels
        labels = (  ('Flight Nº', 0, 1),
                    ('Time', 0, 2),
                    ('Inbound', 1, 0),
                    ('Outbound', 2, 0)  )
        for tup in labels:
            ttk.Label(flight_window,
                        text=tup[0]).grid(row=tup[1],
                                        column=tup[2], **label_G_options)

        # input fields as text boxes
        in_no = Text(width=10, **text_M_options)
        in_time = Text(width=7, **text_M_options)
        out_no = Text(width=10, **text_M_options)
        out_time = Text(width=7, **text_M_options)

        boxes = (   (in_no, 1, 1),
                    (in_time, 1, 2),
                    (out_no, 2, 1),
                    (out_time, 2, 2)    )
        for tup in boxes:
            tup[0].grid(row=tup[1], column=tup[2], padx=20)

        # save and cancel buttons #
        ttk.Button(flight_window, text='Save', width=5,
            command=lambda: save(1, flight_window, [in_no,
                                                    in_time,
                                                    out_no,
                                                    out_time])).grid(
                                                            row=3, column=2,
                                                            padx=10, pady=10)
        ttk.Button(flight_window, text='Cancel', width=7,
                command=flight_window.destroy).grid(row=3, column=1,
                                                    padx=10, pady=20,
                                                    sticky=E)


# create function to accept details of other type of clean #
def other_clean():

    if c_selection.get() == 'o':
        # create other clean frame
        oc_window = Toplevel(bg='#f9f5f0')
        oc_window.title('Specify Other Type')

        # create description box and label
        ttk.Label(oc_window, text='Clean Description', font='Nato 11').grid(
                                row=0, column=0, padx=20, pady=10, sticky=W)
        description_box = Text(oc_window, width=17, height=1, font='Arial 11')
        description_box.grid(row=1, column=0, padx=20, sticky=W)

        # create charge box and labels
        ttk.Label(oc_window, text='Charge', font='Nato 11').grid(
                                    row=0, column=1, padx=0, pady=10, sticky=W)
        ttk.Label(oc_window, text='(€)', font='Nato 11').grid(
                                    row=1, column=1, padx=0, pady=10, sticky=W)
        charge_box = Text(oc_window, width=6, height=1, font='Arial 11')
        charge_box.grid(row=1, column=1, padx=30, sticky=W)

        # save and cancel buttons
        ttk.Button(oc_window, text='Save', width=5,
                command=lambda: save(2, oc_window, [description_box,
                                                    charge_box])
                                                    ).grid(row=3, column=1,
                                                            padx=10, pady=10)
        ttk.Button(oc_window, text='Cancel',
                command=oc_window.destroy, width=7).grid(row=3, column=0,
                                                            columnspan=2,
                                                            padx=10, pady=20)

# function to provide custom charge description in a pop-up window #
def custom_charge_description(var):

    # create pop-up window to take in custom charge description
    custom_window = Toplevel(bg='#fbf9f6')
    custom_window.title('Add details for charge')
    # create label to ask for description
    ttk.Label(custom_window, text='Description',background='#fbf9f6').grid(
                                row=0, column=0, padx=20, pady=10, sticky=W)
    # create box to take in description
    description_box = Text(custom_window, width=17, height=1,
                                font='Arial 11')
    description_box.grid(row=1, column=0, padx=20, sticky=W)

    # save and cancel buttons #
    ttk.Button(custom_window, text='Save', width=5,
            command=lambda: save(var, custom_window, [description_box])
                        ).grid(row=3, column=1, padx=10, pady=10)

    ttk.Button(custom_window, text='Cancel', width=7,
                            command=custom_window.destroy).grid(
                                row=3, column=0, columnspan=2, padx=10, pady=20)



"""CHARGES FRAMES"""
def generate_charges():

    #### OPTIONS ####
    ## Glossary:
        ## _settings = to set instantiation options
        ## _options = to set grid placement options
    # FRAME options
    frame_settings = {  'master': stay_frame,
                        'padx': 0,
                        'pady': 20,
                        'bd': 5,
                        'bg': '#fbf9f6' }
    frame_options = {   'row': 1,
                        'padx': 10,
                        'pady': 10,
                        'sticky': N }
    # TITLE of frame options
    title_settings = {  'bg': '#fbf9f6',
                        'font': 'Helvetica 14 bold' }
    title_options = {   'row': 0,
                        'column': 0,
                        'columnspan': 3,
                        'padx': 20,
                        'pady': 20,
                        'sticky': N }
    # SEPARATOR options
    separator_options = {   'column': 0,
                            'columnspan': 3,
                            'padx': 10,
                            'pady': 0,
                            'ipadx': 180    }
    # COLUMN options in cost listing
    lcol_settings = {   'font': 'Tlwg_Typist 10',
                        'background': '#fbf9f6' }
    lcol_options = {    'column': 0,
                        'padx': 10,
                        'pady': 7,
                        'sticky': E }
    mcol_settings = {   'width': 6,
                        'height': 1,
                        'font': 'Arial 11'  }
    mcol_options = {    'column': 1,
                        'padx': 10,
                        'pady': 7   }
    rcol_settings = {   'font': 'Tlwg_Typist 10 italic',
                        'background': '#fbf9f6',
                        'foreground': '#333333' }
    rcol_options = {    'column': 2,
                        'padx': 7,
                        'pady': 7,
                        'sticky': W }
    # CUSTOM BUTTON options
    button_options = {  'text': 'Add description',
                        'fg': 'dark grey',
                        'font': 'Tlwg_Typist 9 italic',
                        'bg': '#f0f0f0' }
    # options for TOTAL
    ltot_options = {    'column': 0,
                        'padx': 10,
                        'pady': 0,
                        'sticky': E }

    ###FRAMES###
    # create charges frames after first submission
    owner_charges = LabelFrame(**frame_settings).grid(**frame_options,
                                                        column=0)
    guest_charges = LabelFrame(**frame_settings).grid(**frame_options,
                                                        column=1)
    # create title labels
    Label(owner_charges,
            text='Charges to Owner',
            **title_settings
            ).grid(**title_options)
    Label(guest_charges,
            text='Charges to Guest',
            **title_settings
            ).grid(**title_options)

    ####HEADERS####
    # create charges header labels and separator for both frames #
    for frame in (owner_charges, guest_charges):
        ttk.Label(frame,
                    text='Charge',
                    font='Lato 13').grid(row=1,
                                            column=0,
                                            padx=5,
                                            pady=0,
                                            sticky=E)
        ttk.Label(frame,
                    text='Cost (€)',
                    font='Lato 13').grid(row=1,
                                            column=1,
                                            padx=0,
                                            pady=0)
        ttk.Label(frame,
                    text='Details',
                    font='Lato 13').grid(row=1,
                                            column=2,
                                            padx=5,
                                            pady=0,
                                            sticky=W)
        # add separator to underline the column headers
        ttk.Separator(frame,
                        orient='horizontal').grid(row=2,
                                                    **separator_options)

    """CALCULATING OWNER CHARGES"""
    # create owner charges breakdown #
    # create variable to hold number of people
    total_people = (    int(adult_field.get(1.0, 'end-1c')) +
                        int(child_field.get(1.0, 'end-1c')) +
                        int(baby_field.get(1.0, 'end-1c'))      )

    ###CLEANING CHARGES###
    # create clean charge submission
    ttk.Label(owner_charges,
                text='Cleaning',
                **lcol_settings).grid(row=3,
                                            **lcol_options)
    # produce contents for the charge and details of clean
    if clean_selection.get() == 'y':
        desc1, charge1 = sub.clean_calc(property.get(), total_people)
    elif clean_selection.get() == 'n':
        desc1 = 'No Clean'
        charge1 = '00.00'
    else:
        desc1 = other_clean_dict['description']
        charge1 = other_clean_dict['charge']
    # clean charge box
    owner_clean_box = Text(owner_charges, **mcol_settings)
    owner_clean_box.insert(1.0, charge1)
    owner_clean_box.grid(row=3, **mcol_options)
    # description/details of charge
    ttk.Label(owner_charges,
                text=desc1,
                **rcol_settings).grid(row=3,
                                            **rcol_options)

    ###MEET AND GREET CHARGES###
    # create m&g charge submission
    ttk.Label(owner_charges,
                text='Meet & Greet',
                **lcol_settings).grid(row=4,
                                            **lcol_options)
    # produce contents for the charge and details
    if mg_selection.get() == 'y':
        desc2 = 'Standard'
        charge2 = '25.00'
    else:
        desc2 = 'No Meet & Greet'
        charge2 = '00.00'
    # box to display and edit price
    owner_mg_box = Text(owner_charges, **mcol_settigs)
    owner_mg_box.insert(1.0, charge2)
    owner_mg_box.grid(row=4, **mcol_options)
    # description/details of charge
    ttk.Label(owner_charges,
                text=desc2,
                **rcol_settings).grid(row=4,
                                        **rcol_options)

    ###CUSTOME CHARGE###
    # create custom charge option #
    ttk.Label(owner_charges,
                text='Custom Charge',
                **lcol_settings).grid(row=5,
                                        **lcol_options)
    # create box to edit charge, default is '00.00'
    owner_custom_box = Text(owner_charges, **mcol_settings)
    owner_custom_box.insert(1.0, '00.00')
    owner_custom_box.grid(row=5, **mcol_options)
    # create button for description option

    owner_custom_button = Button(owner_charges,
                                    **button_options,
                                    command=lambda: custom_charge_description(3))
    owner_custom_button.config(width=10, height=1)
    owner_custom_button.grid(row=5, **rcol_options)

    # create a calculation separator to emphasise item and total distinction
    ttk.Separator(owner_charges,
                    orient='horizontal').grid(row=6,
                                                **separator_options)

    ###TOTAL###
    # create row for total charge to owner and calculate it
    ttk.Label(owner_charges,
                text='TOTAL',
                **lcol_settings).grid(row=7,
                                    **ltot_options)
    # calculate total, produce alternative text for bad values
    try:
        owner_total = format(
                                float(owner_clean_box.get(1.0, 'end-1c')) +
                                float(owner_mg_box.get(1.0, 'end-1c')) +
                                float(owner_custom_box.get(1.0, 'end-1c')),
                                '.2f')

    except:
        owner_total = 'BAD VALUES'
        ttk.Label(owner_charges,
                    text='Check nºs and retry',
                    font='Tlwg_Typist 9 bold',
                    background='#fbf9f6',
                    foreground='#333333').grid(row=7,
                                                column=2,
                                                padx=7,
                                                pady=0,
                                                sticky=W)
    # display total
    ttk.Label(owner_charges,
                text=owner_total).grid(row=7,
                                        column=1,
                                        padx=10,
                                        pady=0)


    """CALCULATING GUEST CHARGES"""
    # create conditions to generate guest list of guest charges #
    list_guest_charges = []

    # check for late meet and greet fee #
    if transport_selected.get() == 'Flight':
        try:
            if (int(flight_dict['in_time'].get(1.0, 'end-1c')[0:2]) >= 18 or
                int(flight_dict['in_time'].get(1.0, 'end-1c')[0:2]) <= 3):
                list_guest_charges.append([
                                            'Meet & Greet',
                                            '20.00',
                                            'Late Fee'
                                            ])
        except:
            if (int(flight_dict['in_time'].get(1.0, 'end-1c')[0:1]) <= 3 and
                len(flight_dict['in_time'].get(1.0, 'end-1c')) == 4):
                list_guest_charges.append([
                                            'Meet & Greet',
                                            '20.00',
                                            'Late Fee'
                                            ])
    else:
        if int(eta_hrs.get()) >= 20 or int(eta_hrs.get()) <= 3:
            list_guest_charges.append([
                                        'Meet & Greet',
                                        '20.00',
                                        'Late Fee'
                                        ])

    # check for airport transfer and calculate fee #
    if at_var.get() == 'y':
        if total_people <= 4:
            list_guest_charges.append([
                                        'Airport Transfer',
                                        '79.00',
                                        str(total_people) + ' people'
                                        ])
        else:
            list_guest_charges.append([
                                        'Airport Transfer',
                                        '94.00',
                                        str(total_people) + ' people'
                                        ])

    # check for welcome pack #
    if wp_var.get() == 'y':
        list_guest_charges.append([
                                    'Welcome Pack',
                                    '30.00',
                                    'Standard'
                                    ])

    # calculate stay length to measure charges for cot and high chair rental
    #stay_length = sub.stay_length_calc(arrival_str, departure_str)
    # check for high chair and cot
    if hc_var.get() == 'y' and cot_var.get() == 'y':
        if stay_length <= 10:
            list_guest_charges.append([
                                        'Cot & High Chair',
                                        '30.00',
                                        'Short Rental'
                                        ])
        else:
            list_guest_charges.append([
                                        'Cot & High Chair',
                                        '40.00',
                                        'Long Rental'
                                        ])
    elif hc_var.get() == 'y':
        if stay_length <= 10:
            list_guest_charges.append([
                                        'High Chair',
                                        '20.00',
                                        'Short Rental'
                                        ])
        else:
            list_guest_charges.append([
                                        'High Chair',
                                        '30.00',
                                        'Long Rental'
                                        ])
    elif cot_var.get() == 'y':
        if stay_length <= 10:
            list_guest_charges.append([
                                        'Cot',
                                        '20.00',
                                        'Short Rental'
                                        ])
        else:
            list_guest_charges.append([
                                        'Cot',
                                        '30.00',
                                        'Long Rental'
                                        ])

    # place guest charges on the screen
    global row_count
    row_count = 3
    guest_total = 0
    if len(list_guest_charges) == 0:
        Label(guest_charges,
                text='There are no auto-generated charges').grid(row=row_count,
                                                                column=0,
                                                                columnspan=3,
                                                                padx=5,
                                                                pady=10)
        row_count +=1
    else:

        for item in list_guest_charges:

            ttk.Label(guest_charges,
                        text=item[0],
                        **lcolumn_M_options).grid(row=row_count,
                                                    **lcolumn_G_options)

            charge_box = Text(guest_charges,
                                **ccolumn_M_options)
            charge_box.insert(1.0, item[1])
            charge_box.grid(row=row_count,
                                **ccolumn_G_options)

            ttk.Label(guest_charges,
                        text=item[2],
                        **rcolumn_M_options).grid(row=row_count,
                                                    **rcolumn_G_options)

            guest_total += float(item[1])
            row_count +=1


    '''Custom Charge'''
    # create custom charge option
    ttk.Label(guest_charges,
                text='Custom Charge',
                **lcolumn_M_options).grid(row=row_count,
                                            **lcolumn_G_options)
    guest_custom_box = Text(guest_charges, **ccolumn_M_options)
    guest_custom_box.insert(1.0, '00.00')
    guest_custom_box.grid(row=row_count, **ccolumn_G_options)
    # create button for description option
    global guest_custom_button
    guest_custom_button = Button(guest_charges,
                                    **custom_button_options,
                                    command=lambda: custom_charge_description(4))
    guest_custom_button.config(width=10, height=1)
    guest_custom_button.grid(row=row_count, **rcolumn_G_options)

    # create a calculation separator to emphasise item and total distinction
    ttk.Separator(guest_charges,
                    orient='horizontal').grid(row=row_count+1,
                                                    **separator_options)

    # create row for total charge to guest and calculate it
    ttk.Label(guest_charges,
                text='TOTAL',
                **lcolumn_M_options).grid(row=row_count+2,
                                            **ltotal_G_options)
    ttk.Label(guest_charges,
                text=format(guest_total, '.2f')).grid(row=row_count+2,
                                                                column=1,
                                                                padx=10,
                                                                pady=0)




"""CHECK SUBMISSION"""
# function called when 'Generate Charges' button pressed
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
    generate_charges()


#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#### OPTIONS ####
## Glossary:
    ## _settings = to set instantiation options
    ## _options = to set grid placement options
frame_settings = {  'master': stay_frame,
                    'bd': 5,
                    'bg': '#f9f5f0' }
title_settings = {  'font': 'Helvetica 16 bold',
                    'bg': '#f9f5f0' }
title_options = {   'row': 0,
                    'column': 0,
                    'columnspan': 2,
                    'pady': 20,
                    'sticky': N }
radioY_settings = { 'text': 'Yes',
                    'value': 'y'    }
radioN_settings = { 'text': 'No',
                    'value': 'n'    }
radio_options = {   'column': 1,
                    'padx': 21  }
cal_settings = {    'selectmode': 'day',
                    'locale': 'en_UK',
                    'font': 'Arial 11',
                    'showweeknumbers': False,
                    'showothermonthdays': False,
                    'weekendbackground': '#ededed',
                    'weekendforeground': 'black',
                    'width': 14 }

'''Create 3 initial frames and put them on grid'''
main = LabelFrame(**frame_settings, padx=30, pady=30)
management = LabelFrame(**frame_settings, padx=35, pady=30)
extras = LabelFrame(**frame_settings, padx=33, pady=35)

frames = ((frame_main, 0, N), (frame_clean, 1, N), (frame_extras, 1, S))
for tup in frames:
    tup[0].grid(row=0, column=tup[1], padx=10, pady=10, sticky=tup[2])


'''MAIN FRAME'''
# call on Property class for generation and interactivity of first 2 rows
property = cl.Property(main)

#####LABELS####
# create labels of column 0 of Main Frame and place on grid
main_labels = ('Owner',
                'Guest',
                'Email',
                'Party Composition',
                'Arriving',
                'Departing',
                'Transportation',
                'Hiring a Car',
                'ETA')

row_count = 2
for item in main_labels:
    if item == 'Party Composition': # skip party comp row, will use frame instead
        row_count += 1
    else:
        ttk.Label(main,
                    text=item).grid(row=row_count, column=0,
                                     padx=20, pady=10,
                                     sticky=W)
        row_count += 1

# create radio button for owner #
owner_selection = StringVar()
owner_selection.set('n')
ttk.Radiobutton(main,
                **radioY_settings,
                variable=owner_selection).grid(row=2,
                                                **radio_options,
                                                sticky=W)
ttk.Radiobutton(main,
                **radioN_settings,
                variable=owner_selection).grid(row=2,
                                                **radio_options,
                                                sticky=E)

#####FIELDS####

# guest name and email text fields, on rows 3 and 4
for n in range(3, 5):
    Text(main,
            width=24, height=1,
            font='Arial 11').grid(row=n, column=0,
                                    columnspan=2,
                                    padx=20, pady=0,
                                    sticky=E)

# create internal frame for party composition labels fields #
# initiate frame
party_frame = LabelFrame(main,
                            padx=0, pady=0,
                            bd=0, bg='#f9f5f0')
party_frame.grid(row=5, column=0,
                    columnspan=2,
                    padx=20, pady=10,
                    sticky=W)
# create conditions for loop placement of labels/fields in frame
party_labels = ('Adults ', 'Children ', 'Babies ')
for tup in party_labels:
    ttk.Label(party_frame, text=tup).pack(side=LEFT)
    field = Text(party_frame, width=1, height=1, font='Arial 11', bg='#EBECF0')
    if tup == 'Adults ':
        field.insert(1.0, '2')
    else:
        field.insert(1.0, '0')
    field.pack(side=LEFT)

# setting arrival and departure dates #
# declare string variables for dates
arrival_str = StringVar()
departure_str = StringVar()
# labels for the calendar inputs
# initialise and place arrival and departure calendars
DateEntry(main,
            textvariable=arrival_str,
            **cal_settings).grid(row=6, column=1)
DateEntry(main,
            textvariable=departure_str,
            **cal_settings).grid(row=7, column=1)

# create a check for mode of transportation #
# use a list to prepare items to display in dropdown
transport_items = [
        'Flight',
        'Car',
        'Train',
        'Bus'
        ]
# set variable to hold selection
transport_selection = StringVar()
transport_selection.set('Coming by...')
transport_field = OptionMenu(main,
                                transport_selection,
                                *transport_items,
                                command=transport_option)
transport_field.config(width=12, font='Arial 11', anchor=W, borderwidth=0,
                    bg='white')
transport_field.grid(row=8, column=1, padx=20, pady=0)

# create radio button and variable for car hire #
carhire_selection = StringVar()
carhire_selection.set('n')
ttk.Radiobutton(main,
                **radioY_settings,
                variable=carhire_selection).grid(row=9,
                                                    **radio_options,
                                                    sticky=W)
ttk.Radiobutton(main,
                **radioN_settings,
                variable=carhire_selection).grid(row=9,
                                                    **radio_options,
                                                    sticky=E)

# create dropdown for hours and mins for ETA declaration #
# use combobox for better scrolling

eta_hrs = ttk.Combobox(main, font='Arial 11',
                state='readonly', width=4)
eta_hrs['values'] = ['HH', '00', '01', '02', '03', '04', '05', '06', '07', '08',
                    '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                    '19', '20', '21', '22', '23']
eta_hrs.set('HH')
eta_hrs.grid(row=10, column=1, padx=23, sticky=W)

eta_mins = ttk.Combobox(main, font='Arial 11',
                    state='readonly', width=4)
eta_mins['values'] = ['MM', '00', '15', '30', '45']
eta_mins.set('MM')
eta_mins.grid(row=10, column=1, padx=23, sticky=E)


#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>

"""MANAGEMENT FRAME"""
# OPTIONS #
label_settings = {  'master': management,
                    'font': 'Nexa 12 bold',
                    'bg': '#f9f5f0' }
label_options = {   'column': 0,
                    'columnspan': 2,
                    'pady': 20,
                    'sticky': W }
clean_settings = {  'master': clean_types,
                    'highlightthickness': 0,
                    'variable': clean_selection,
                    'command': other_clean,
                    'font': 'Arial 11',
                    'bg': '#f9f5f0'     }
clean_options = {   'column': 0,
                    'padx': 0,
                    'pady': 5,
                    'sticky': W}
mg_settings = {     'master': management,
                    'highlightthickness': 0,
                    'variable': mg_selection,
                    'font': 'Arial 11',
                    'bg': '#f9f5f0'     }
mg_options = {      'row': 6,
                    'column': 1,
                    'pady': 5   }

## Title
# create title for the management frame
Label(management,
        text='Management Services',
        **title_settings).grid(**title_options, padx=40)

####LABELS####
# cleaning label
Label(**label_settings,
        text='Clean Type').grid(row=2, padx=50, **label_options)
# make gap label
Label(**label_settings,
        text='').grid(row=5)
# m&g label
Label(**label_settings,
        text='Meet & Greet').grid(row=6, padx=28, **label_options)

# create cleaning options #
# create frame to stack cleaning options
clean_types = LabelFrame(management, padx=0, pady=10, bd=0, bg='#f9f5f0')
clean_types.grid(row=2, column=1, padx=30, pady=3, sticky=E)
# variable to store selection
clean_selection = StringVar()
clean_selection.set('y')
# radio buttons inside the stacking frame
Radiobutton(clean_types, text='Full Clean', value='y',
            **clean_settings).grid(row=0, **clean_options)
Radiobutton(clean, text='No Clean', value='n',
            **clean_settings).grid(row=1, **clean_options)
Radiobutton(clean_types, text='Other Type', value='o',
            **clean_settings).grid(row=2, **clean_options)

# create m&g options #
# create variable and radio buttons for meet & greet
mg_selection = StringVar()
mg_selection.set('y')
Radiobutton(**mg_settings, text='Yes', value='y').grid(**mg_options,
                                                        padx=77, ipadx=0,
                                                        sticky=E)
Radiobutton(**mg_settings, text='No', value='n').grid(**mg_options,
                                                        padx=20,
                                                        sticky=E)


#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>

"""EXTRAS FRAME"""

# create title label of extras
Label(extras, text='Extras for Guest',
        **title_settings).grid(**title_options)

# initialise variables for extras #
airport_transfer = StringVar()
welcome_pack = StringVar()
cot = StringVar()
high_chair = StringVar()

extras_list = ( ('Airport Transfer', airport_transfer, 1, 0),
                ('Welcome Pack', welcome_pack, 2, 0),
                ('Cot', cot, 2, 1),
                ('High Chair', high_chair, 1, 1)
                )

for tup in extras_list:
    ttk.Checkbutton(extras,
                    text=tup[0],
                    variable=tup[1],
                    onvalue='y',
                    offvalue='n').grid(row=tup[2], column=tup[3],
                                        padx=20, pady=5,
                                        sticky=W)


#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>
#<<<<<<<<<<<<<<<<<<------------------------------------------->>>>>>>>>>>>>>>>>>

# button to submit initial details and perform checks
submit = Button(root, text='Generate Charges', command=check_submission,
            font='San_Francisco 12', background='white')
submit.grid(row=1, column=0, columnspan=2, padx=20, pady=20, ipadx=30, sticky=S)



root.mainloop()
