from tkinter import *
from tkinter import messagebox, ttk, Text, font
from tkcalendar import Calendar, DateEntry
import sqlite3
from functions import set_date, clean_calc, count_days
from datetime import date
from copy import deepcopy



""".........................................................................."""
""".........................................................................."""
##### class to generate the labels, fields and events of the Main Frame #####
class Stay:

    #### OPTIONS ####
    ## Glossary:
        ## _settings = to set instantiation options
        ## _options = to set grid placement options
    frame_settings = {  'bd': 5,
                        'bg': '#f9f5f0'
                        }
    title_settings = {  'bg': '#f9f5f0'
                        }
    title_options = {   'row': 0, 'column': 0,
                        'columnspan': 2,
                        'padx': 15,
                        'sticky': N
                        }
    label_settings = {  'font': 'Nexa 10',
                        'background': '#f9f5f0'
                        }
    label_options = {
                        'row': 1, 'column': 0,
                        'padx': 20, 'pady': 10,
                        'sticky': W
                        }
    field_options = {
                        'row': 1, 'column': 0,
                        'columnspan': 2,
                        'padx': 20, 'pady': 5,
                        'sticky': E
                        }
    radioY_settings = { 'text': 'Yes',
                        'value': 'y'
                        }
    radioN_settings = { 'text': 'No',
                        'value': 'n'
                        }
    radio_options = {   'column': 1,
                        }
    cal_settings = {    'selectmode': 'day',
                        'locale': 'en_UK',
                        'font': 'Arial 11',
                        'showweeknumbers': False,
                        'showothermonthdays': False,
                        'weekendbackground': '#ededed',
                        'weekendforeground': 'black',
                        'width': 11
                        }


    # initialise class by inheriting and declaring frame and setting title
    def __init__(self, frame, type, *id):

        self.frame =    frame
        self.type =     type

        if id:
            self.id =   id[0]


        # create 3 frames
        self.first =        LabelFrame(     self.frame,
                                            **self.frame_settings,
                                            padx=25, pady=25
                                            )
        self.second =       LabelFrame(     self.frame,
                                            **self.frame_settings,
                                            padx=25, pady=25
                                            )
        self.management =   LabelFrame(     self.frame,
                                            **self.frame_settings,
                                            padx=25, pady=25
                                            )
        self.extras =       LabelFrame(     self.frame,
                                            **self.frame_settings,
                                            padx=25, pady=25
                                            )

        # put them on grid and add titles
                            #name,row,column,sticker, title
        frames = (  (self.first, 0, 1, N, 'Guest & Property'   ),
                    (self.second, 1, 1, N, 'Dates & Transport'   ),
                    (self.management, 0, 2, N, 'Management'     ),
                    (self.extras, 1, 2, N, 'Guest Extras'       )
                    )

        # iterate over the tuple
        for tup in frames:

            tup[0].grid(                row=tup[1], column=tup[2],
                                        padx=10, pady=10,
                                        sticky=tup[3]
                                        )
            # also add titles, exception for first frame where title will change
            if tup[0] == self.first:
                self.title = Label(     tup[0],
                                        text=tup[4],
                                        font='Helvetica 13 bold',
                                        **self.title_settings
                                        )
                self.title.grid(        pady=10,
                                        **self.title_options
                                        )
            else:
                Label(
                                        tup[0],
                                        text=tup[4],
                                        font='Helvetica 13 bold',
                                        **self.title_settings
                    ).grid(
                                        pady=10,
                                        **self.title_options
                                        )


        # call on functions in class that will populate these 3 frames
        self.build_prop_list()
        self.set_variables()
        self.build_first()
        self.build_second()
        self.build_management()
        self.build_extras()

        # buttons for different conditions, one for new stay, another for update
        if self.type == 'new':
            # create and place CHARGES button
            self.gen_charges = Button(  self.frame,
                                        text='Generate Charges',
                                        command=self.check_submission,
                                        font='San_Francisco 10',
                                        background='white'
                                    )
            self.gen_charges.grid(      row=2, column=1,
                                        columnspan=2,
                                        padx=20, pady=20, ipadx=20,
                                        sticky=S
                                    )

        else:
            self.generate_charges(pull=True)


    # function to set variables of the Stay Window of the application
    def set_variables(self):

        ###MAIN FRAME VARS###
        self.name =             'Select from...'
        self.owner =            StringVar()
        self.guest =            StringVar()
        self.email =            StringVar()
        self.adults =           StringVar()
        self.kids =             StringVar()
        self.babies =           StringVar()
        self.arrival =          StringVar()
        self.departure =        StringVar()
        self.transport =        StringVar()
        self.carhire =          StringVar()
        self.eta_hrs =          StringVar()
        self.eta_mins =         StringVar()
        self.security =         StringVar()

        ###FLIGHT WINDOW###
        self.in_no =            StringVar()
        self.in_time =          StringVar()
        self.out_no =           StringVar()
        self.out_time =         StringVar()

        ###MANAGEMENT VARS###
        self.clean =            StringVar()
        self.meetgreet =        StringVar()

        ###EXTRAS VARS###
        self.airport_transfer = StringVar()
        self.welcome_pack =     StringVar()
        self.cot =              StringVar()
        self.high_chair =       StringVar()

        ###OWNER CHARGES VARS###
        #only set clean and meetgreet if pulling from database
        self.clean_charge =         StringVar()
        self.clean_desc =           StringVar()
        self.meetgreet_charge =     StringVar()
        self.meetgreet_desc =       StringVar()
        self.custom_owner_charge =  StringVar()
        self.custom_owner_desc =    StringVar()
        self.owner_total =          0.0

        ###GUEST CHARGES VARS###
        # create a list of guest charges #
        # initiate variables to hold the charges in the entry boxes
        # set initial variables to standard prices, to be changed on condition
        self.guest_meetgreet_charge =   StringVar()
        self.guest_meetgreet_desc =     StringVar()
        self.transfer_charge =          StringVar()
        self.transfer_desc =            StringVar()
        self.transfer_edited =          False
        self.pack_charge =              StringVar()
        self.pack_desc =                StringVar()
        self.pack_edited =              False
        self.cotchair_charge =          StringVar()
        self.cotchair_desc =            StringVar()
        self.cotchair_edited =          False
        self.list_guest_charges =       list()
        self.custom_guest_charge =      StringVar()
        self.custom_guest_desc =        StringVar()
        self.guest_total =              0.0


        #######SET VARS#######
        if self.type == 'new':

            ###MAIN FRAME VARS###
            self.owner.set('n')
            self.guest.set('')
            self.email.set('')
            self.adults.set('2')
            self.kids.set('0')
            self.babies.set('0')
            # use function in F module to set automated arrival date to 2 weeks' time
            # and automated departure date to 3 weeks' time
            # only set variables to give to stringvars after calendars have been init
            self.arrival_date =     set_date(   date.today().strftime('%d/%m/%Y'),
                                                'a'
                                                )
            self.departure_date =   set_date(   date.today().strftime('%d/%m/%Y'),
                                                'd'
                                                )
            self.transport.set('Coming by...')
            self.carhire.set('n')
            self.eta_hrs.set('HH')
            self.eta_mins.set('MM')
            self.security.set('n')

            ###FLIGHT WINDOW###
            self.in_no.set('')
            self.in_time.set('')
            self.out_no.set('')
            self.out_time.set('')

            ###MANAGEMENT VARS###
            self.clean.set('y')
            self.meetgreet.set('y')

            ###EXTRAS VARS###
            self.airport_transfer.set('n')
            self.welcome_pack.set('n')
            self.cot.set('n')
            self.high_chair.set('n')

            ###OWNER CHARGES VARS###
            self.custom_owner_charge.set('0.00')
            self.custom_owner_desc.set('Add description')

            ###GUEST CHARGES VARS###
            self.guest_meetgreet_charge.set('20.00')
            self.guest_meetgreet_desc.set('Late fee')
            self.transfer_charge.set('79.00')
            self.transfer_desc.set('2 ways - 2 pax')
            self.pack_charge.set('30.00')
            self.pack_desc.set('Standard')
            self.cotchair_charge.set('20.00')
            self.cotchair_desc.set('Short Rental')
            self.custom_guest_charge.set('0.00')
            self.custom_guest_desc.set('Add description')


        else:

            self.database_pull()



    def build_prop_list(self, type='stay'):

        # call on DB Properties Table and name column to make list to append
        self.lst = ['Select from...']
        # connect to DB
        conn = sqlite3.connect('KKLJ.db')
        cur = conn.cursor()
        # execute sql code to retrieve relevant data
        cur.execute('SELECT name FROM Properties')
        self.properties = cur.fetchall()

        if type == 'stay':

            # iterate over retrieved data to append to list
            # fetchall() returns a list of tuples, need to iterate twice
            for tup in self.properties:

                for property in tup:
                    # shorten long property names

                    if property[0:2] == 'Qu':       # look for Quinta da Barracuda
                        self.lst.append('Qta. Barracuda - ' + property[-3:])

                    elif property[0:2] == 'Pa':     # look for Parque da Corcovada

                        if property[-5] == ' ':     # PdQ names have diff lengths
                            self.lst.append('Pq. Corcovada - ' + property[-4:])
                        else:
                            self.lst.append('Pq. Corcovada - ' + property[-5:])

                    elif property[0:2] == 'Cl':     # look for Clube do Monaco

                        if property[-2] == ' ':     # CdM also have diff lengths
                            self.lst.append('Clb. Monaco - ' + property[-1])
                        else:
                            self.lst.append('Clb. Monaco - ' + property[-2:])

                    else:
                        self.lst.append(property)

        if type == 'pull':

            pull_list = list()

            for tup in self.properties:

                for property in tup:

                    pull_list.append(property)

            return pull_list


        conn.close()


    # start the 4 tiered process of building the main frame of the Stay Window
    # starts with setting the labels for each field, then creates
    # property, guest, party size, time events and transport fields
    # finally producing interactive display of property and owner selection
    def build_first(self):

        #####LABELS####
        # create labels of column 0 and place on grid
        # exception 1 for 'Property' label which will be manipulated
        # exception 2 for party size which will be handled by internal frame
        first_labels = (    'Property',
                            'Owner',
                            'Guest',
                            'Email'
                            #'Party Composition', excluded and placed separately
                            )

        row_count = 1 # starting count for row num to loop

        for item in first_labels:
        # property labels needs to be callable
            if item == 'Property':

                self.label = ttk.Label( self.first,
                                        text='Property',
                                        **self.label_settings
                                        )
                self.label.grid(        row=row_count,
                                        column=0,
                                        padx=15,
                                        pady=5,
                                        sticky=W
                                        )
                row_count += 1

            else:
                ttk.Label(      self.first,
                                text=item,
                                **self.label_settings
                    ).grid(     row=row_count,
                                column=0,
                                padx=15,
                                pady=5,
                                sticky=W
                                )
                row_count += 1


        # build the fields for the first 5 rows (title,property,guest info, party_size)
        self.property_and_guest()




    # function to define the appearance of the first 5 rows which are heavily
    # dependent on one another: title, property, owner select, guest name & email
    def property_and_guest(self):

        ##set initial property name to generic 'Select from...'
        #simplifies call on getter for property by the Check function of App Calss
        # make Combobox to list properties
        self.property_selection = ttk.Combobox( self.first,
                                                width=18,
                                                values=self.lst,
                                                state='readonly',
                                                font=('Courier New', '10')
                                                )
        # set first option as generic
        self.property_selection.set(            self.name
                                                )
        # set choice in box to activate chage of title of the Main Frame
        self.property_selection.bind(           '<<ComboboxSelected>>',
                                                self.property_appearance
                                                )
        self.property_selection.grid(           **self.field_options
                                                )

        ## look for database pull
        if self.name != 'Select from...':
            self.property_appearance()


        # create radio button for owner #
        # will affect next 2 rows guest and email fields depending on selection
        owner_yes = ttk.Radiobutton(    self.first,
                                        **self.radioY_settings,
                                        variable=self.owner,
                                        command=self.owner_setting
                                        )
        owner_yes.grid(                 row=2,
                                        column=1,
                                        padx=0,
                                        sticky=W
                                        )
        owner_no = ttk.Radiobutton(     self.first,
                                        **self.radioN_settings,
                                        variable=self.owner,
                                        command=self.owner_setting
                                        )
        owner_no.grid(                  row=2,
                                        column=1,
                                        padx=20,
                                        sticky=E
                                        )


        # guest NAME and EMAIL text fields, on rows 3 and 4
        name_email = (      (self.guest, 3  ),      # variable, row
                            (self.email, 4  )
                            )

        for tup in name_email:
            field = Entry(  self.first,
                            textvariable=tup[0],
                            width=22,
                            font='Arial 9'
                            )
            field.grid(     row=tup[1], column=0,
                            columnspan=2,
                            padx=20, pady=0,
                            sticky=E
                            )


        # starting at row 5, after property, owner select, guest name and email
        # create internal frame for party composition labels fields #
        # initiate frame
        party_frame = LabelFrame(   self.first,
                                    padx=0, pady=0,
                                    bd=0, bg='#f9f5f0'
                                    )
        party_frame.grid(           row=5, column=0,
                                    columnspan=2,
                                    padx=15, pady=10,
                                    ipadx=2,
                                    sticky=E
                                    )

        # create conditions for loop placement of labels/fields in frame
        # initialise variable to hold input
        party_labels = (        ('Adults', self.adults      ),
                                ('   ',                     ),
                                ('Children', self.kids      ),
                                ('   ',                     ),
                                ('Babies', self.babies      )
                                )
        column_count = 0
        for tup in party_labels:

            ttk.Label(
                        party_frame,
                        text=tup[0],
                        **self.label_settings
                ).grid(
                        row=0,
                        column=column_count
                        )
            column_count += 1

            if tup[0] != '   ':
                field = Entry(
                                party_frame,
                                textvariable=tup[1],
                                width=2,
                                justify=RIGHT,
                                font='Arial 9',
                                bg='#EBECF0'
                                )
                field.grid(
                                row=0,
                                column=column_count
                                )
                column_count += 1


    # function to change the title to property headline once property selected #
    def property_appearance(self, *var):

        #check for change in the selection of property
        if self.property_selection.get() != 'Select from...':

            # remove first appearance title and property selection label and field
            self.title.grid_remove()
            self.label.grid_remove()
            self.property_selection.grid_remove()

            # find full name of selected property to display as new title
            for tup in self.properties:
                for property in tup:
                    # find correct full name by selecting ending of listed prop
                    if property[-5:] == self.property_selection.get()[-5:]:
                        self.name = property

            # generate title with property name
            self.property = Label(      self.first,
                                        text=self.name,
                                        bg='#f9f5f0',
                                        font='Helvetica 13 bold'
                                        )
            self.property.grid(         row=0, column=0, columnspan=2,
                                        padx=20, pady=4, sticky=N
                                        )

            ###RESET###
            # give button option to reset to property selection
            self.reset = Button(        self.first,
                                        text='Change Property',
                                        command=self.reset_appearance,
                                        fg='dark grey',
                                        font='San_Fancisco 8',
                                        bg='#f0f0f0'
                                        )
            self.reset.grid(            row=1, column=0, columnspan=2,
                                        padx=20, pady=10
                                        )



    # function to change property selection again #
    def reset_appearance(self):

        # remove changed elements
        self.property.grid_remove()
        self.reset.grid_remove()
        #restore first appearance
        self.title.grid(                **self.title_options
                                        )
        self.label.grid(                padx=15,
                                        pady=5,
                                        sticky=W
                                        )
        self.property_selection.set(    'Select from...'        )
        self.property_selection.grid(   **self.field_options    )
        # also reset the owner choice option and get rid of any leftover
        # owner name and email in the respective fields
        self.owner_resetting()



    # function to follow owner selection, and auto-fill name and email if selected
    def owner_setting(self):

        # check if fucntion call is to set owner details
        if self.property_selection.get() != 'Select from...':

            if self.owner.get() == 'y':
                conn = sqlite3.connect('KKLJ.db')
                cur = conn.cursor()
                cur.execute(    'SELECT owner,email FROM Properties WHERE name=?',
                                (self.name,)
                                )
                content = cur.fetchone()
                self.guest.set(content[0])
                self.email.set(content[1])
                self.security.set('n')
                self.meetgreet.set('n')

            else:
                self.guest.set('')
                self.email.set('')
                self.security.set('y')
                self.meetgreet.set('y')

        else:
            messagebox.showerror(   'No Property',
                                    'Please select a property first.'
                                    )
            self.owner.set('n')
            return



    # function called to reset owner to 'no' and remove owner details
    # when property selection is reset
    def owner_resetting(self):

        if (    self.property_selection.get() == 'Select from...'
            and
                self.owner.get() == 'y'
        ):
            self.owner.set('n')
            self.guest.set('')
            self.email.set('')
            self.security.set('y')
            self.meetgreet.set('y')




    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    def build_second(self):

        #####LABELS####
        # create labels of column 0 and place on grid
        # exception 1 for 'Property' label which will be manipulated
        # exception 2 for party size which will be handled by internal frame
        second_labels = (   'Arrival',
                            'Departure',
                            'Transportation',
                            'Hiring a Car',
                            'ETA'
                            )

        row_count = 1 # starting count for row num to loop

        for item in second_labels:

            ttk.Label(      self.second,
                            text=item,
                            **self.label_settings
                ).grid(     row=row_count,
                            column=0,
                            padx=15,
                            pady=5,
                            sticky=W
                            )
            row_count += 1


        # build fields of next 5 rows of the frame (times and transport)
        self.times_and_transport()



    # function to set the fields for the other 7 rows of the main frame
    # party size, in and out dates, mode of transport, car hire, eta, security dep
    def times_and_transport(self):


        # labels for the calendar inputs
        # initialise and place arrival and departure calendars
        arrival_cal = DateEntry(    self.second,
                                    textvariable=self.arrival,
                                    **self.cal_settings
                                    )
        arrival_cal.grid(           row=1, column=1, pady=5
                                    )
        departure_cal = DateEntry(  self.second,
                                    textvariable=self.departure,
                                    **self.cal_settings
                                    )
        departure_cal.grid(         row=2, column=1, pady=5
                                    )

        self.arrival.set(           self.arrival_date       )
        self.departure.set(         self.departure_date     )

        # create a check for mode of TRANSPORTATION #
        # use a list to prepare items to display in dropdown
        transport_items = [
                            'Flight',
                            'Car',
                            'Train',
                            'Bus'
                            ]
        # set variable to hold selection

        #self.transport_selection.set('Coming by...')
        # call on check_transport() to decide if flight details window is necessary
        transport_field = OptionMenu(   self.second,
                                        self.transport,
                                        *transport_items,
                                        command=self.transport_check
                                        )
        transport_field.config(         width=10, font='Arial 10', bg='white',
                                        anchor=W, borderwidth=0
                                        )
        transport_field.grid(           row=3, column=1, padx=20, pady=5
                                        )


        #self.carhire_selection.set('n')
        carhire_yes = ttk.Radiobutton(      self.second,
                                            **self.radioY_settings,
                                            variable=self.carhire
                                            )
        carhire_yes.grid(                   row=4,
                                            column=1,
                                            padx=18,
                                            pady=5,
                                            sticky=W
                                            )
        carhire_no = ttk.Radiobutton(       self.second,
                                            **self.radioN_settings,
                                            variable=self.carhire
                                            )
        carhire_no.grid(                    row=4,
                                            column=1,
                                            padx=18,
                                            pady=5,
                                            sticky=E
                                            )


        # create dropdown for hours and mins for ETA declaration #
        # use combobox for better scrolling
        eta_hrs = ttk.Combobox(     self.second,
                                    textvariable=self.eta_hrs,
                                    font='Arial 10',
                                    state='readonly',
                                    width=3
                                    )
        eta_hrs['values'] = (       'HH', '00', '01', '02', '03', '04', '05',
                                    '06', '07', '08', '09', '10', '11', '12',
                                    '13', '14', '15', '16', '17', '18', '19',
                                    '20', '21', '22', '23'
                                    )

        eta_hrs.grid(               row=5, column=1, padx=20, pady=5, sticky=W
                                    )

        eta_mins = ttk.Combobox(    self.second,
                                    textvariable=self.eta_mins,
                                    font='Arial 10',
                                    state='readonly',
                                    width=3
                                    )
        eta_mins['values'] = (      'MM', '00', '15', '30', '45'
                                    )
        eta_mins.grid(              row=5, column=1, padx=20, pady=5, sticky=E
                                    )




    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    # function to populate the management frame in the Stay window
    # options: Clean: full, no, other; Meet & Greet: yer or no
    def build_management(self):

        #### OPTIONS ####
        ## Glossary:
            ## _settings = to set instantiation options
            ## _options = to set grid placement options
        label_settings = {  'font': 'Nexa 10',
                            'fg': '#1f1f1f',
                            'bg': '#f9f5f0'
                            }
        label_options = {   'column': 0,
                            'pady': 10,
                            'sticky': W
                            }
        cln_settings = {    #'highlightthickness': 0,
                            #'font': 'Arial 9',
                            #'bg': '#f9f5f0'
                            }
        cln_options = {     'column': 0,
                            'padx': 0,
                            'pady': 1,
                            'sticky': W
                            }
        mg_settings = {     #'highlightthickness': 0,
                            #'font': 'Arial 9',
                            #'bg': '#f9f5f0'
                            }
        mg_options = {      'row': 4,
                            'column': 1,
                            'pady': 5
                            }

        ####LABELS####
        # cleaning label
        Label(          self.management,
                        **label_settings,
                        text='Clean Type'
            ).grid(
                        row=2, padx=10, **label_options
                        )
        # meetgreet label
        Label(          self.management,
                        **label_settings,
                        text='Meet & Greet'
            ).grid(
                        row=4, padx=10, **label_options
                        )
        # security deposit label
        Label(          self.management,
                        **label_settings,
                        text='Collect Secur.'
            ).grid(
                        row=5, padx=10, **label_options
                        )

        #### CLEANING OPTIONS ####
        # create frame to stack cleaning options
        clean_types = LabelFrame(       self.management,
                                        padx=10, pady=3,
                                        bd=0, bg='#f9f5f0'
                                        )
        clean_types.grid(               row=2, column=1,
                                        padx=15, pady=3,

                                        )


        # call on pop_up() to produce required window if necessary
        # radio buttons inside the stacking frame
        clean_choices = (               (' Full  Clean', 'y', 0   ),
                                        (' No  Clean', 'n', 1     ),
                                        (' Other  Type', 'o', 2   )
                                        )

        for tup in clean_choices:
            radio_field = ttk.Radiobutton(  clean_types,
                                            **cln_settings,
                                            text=tup[0], value=tup[1],
                                            variable=self.clean,
                                            command=self.clean_check
                                            )
            radio_field.grid(               row=tup[2],
                                            **cln_options
                                            )


        # M&G OPTIONS #
        mg_yes = ttk.Radiobutton(   self.management,
                                    **mg_settings,
                                    text='Yes', value='y',
                                    variable=self.meetgreet
                                    )
        mg_yes.grid(                **mg_options,
                                    padx=25, ipadx=0,
                                    sticky=W
                                    )
        mg_no = ttk.Radiobutton(    self.management,
                                    **mg_settings,
                                    text='No', value='n',
                                    variable=self.meetgreet
                                    )
        mg_no.grid(                 **mg_options,
                                    padx=10,
                                    sticky=E
                                    )


        ###SECURITY DEPOSIT###
        security_yes = ttk.Radiobutton(     self.management,
                                            **self.radioY_settings,
                                            variable=self.security,
                                            #bg='#f9f5f0'
                                            )
        security_yes.grid(                  row=5,
                                            column=1,
                                            padx=25, ipadx=0,
                                            sticky=W
                                            )
        security_no = ttk.Radiobutton(      self.management,
                                            **self.radioN_settings,
                                            variable=self.security,
                                            #bg='#f9f5f0'
                                            )
        security_no.grid(                   row=5,
                                            column=1,
                                            padx=10,
                                            sticky=E
                                            )


    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    # fucntion to populate extras frame in the Stay window
    # 4 extras: Airport Transfer, Welcome Pack, Cot, High Chair
    def build_extras(self):

        ##EXTRAS OPTIONS##

        extras_list = ( ('Airport Transfer', self.airport_transfer, 2, 0    ),
                        ('Welcome Pack', self.welcome_pack, 3, 0            ),
                        ('Cot', self.cot, 3, 1                              ),
                        ('High Chair', self.high_chair, 2, 1                )
                        )


        for row in (1, 4):
            Label(
                    self.extras,
                    text=' ',
                    **self.label_settings
            ).grid(
                    row=row,
                    column=0,
                    pady=0
            )

        for tup in extras_list:
            check_extras = ttk.Checkbutton( self.extras,
                                            text=tup[0],
                                            variable=tup[1],
                                            onvalue='y',
                                            offvalue='n'
                                            )
            check_extras.grid(              row=tup[2], column=tup[3],
                                            padx=11, pady=7,
                                            sticky=W
                                            )

        edit_button = Button(   self.extras,
                                text='Edit Extras',
                                font='San_Francisco 10',
                                command=self.edit_extras,
                                fg='black',
                                bg='#f0f0f0'
                                )
        edit_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10)



    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    ###GENERATE AND SAVE POPUP WINDOW DISPLAYS AND INPUT###

    # function to display according to transport method selcted #
    def transport_check(self, var):

        if self.transport.get() == 'Flight':

            # create variable to watch for saved flight information, starts 'n'
            self.flight_info = 'n'

            # create pop-up window to take in flight details
            self.flight_window = Toplevel(  bg='#f9f5f0', padx=5
                                            )
            self.flight_window.title(       'Enter Guest Flight Details'
                                            )

            label_options = {   'sticky': W,
                                'padx': 20,
                                'pady': 10
                                }
            text_settings = {   'master': self.flight_window,
                                'font': 'Arial 11'
                                }

            # head and side labels
            labels = (      ('Flight Nº', 0, 1  ),
                            ('Time', 0, 2       ),
                            ('Inbound', 1, 0    ),
                            ('Outbound', 2, 0   )
                            )
            for tup in labels:
                ttk.Label(
                            self.flight_window,
                            text=tup[0],
                            **self.label_settings
                    ).grid(
                            row=tup[1],
                            column=tup[2],
                            **label_options
                            )

            # make originals before opening window, in case of cancel
            self.in_no_original =       deepcopy(self.in_no.get())
            self.in_time_original =     deepcopy(self.in_time.get())
            self.out_no_original =      deepcopy(self.out_no.get())
            self.out_time_original =    deepcopy(self.out_time.get())

            # input fields as text boxes
            in_no =         Entry(  width=10,
                                    textvariable=self.in_no,
                                    **text_settings
                                    )
            in_time =       Entry(  width=7,
                                    textvariable=self.in_time,
                                    **text_settings
                                    )
            out_no =        Entry(  width=10,
                                    textvariable=self.out_no,
                                    **text_settings
                                    )
            out_time =      Entry(  width=7,
                                    textvariable=self.out_time,
                                    **text_settings
                                    )

            boxes = (       (in_no, 1, 1),
                            (in_time, 1, 2),
                            (out_no, 2, 1),
                            (out_time, 2, 2)
                            )
            for tup in boxes:
                tup[0].grid(row=tup[1], column=tup[2], padx=20)

            # save and cancel buttons #
            ttk.Button(
                        self.flight_window,
                        text='Save', width=5,
                        command=self.flight_window.destroy
                ).grid(
                        row=3, column=2,
                        padx=10, pady=10
                        )
            ttk.Button(
                        self.flight_window,
                        text='Cancel', width=7,
                        command=lambda: self.cancel(1)
                ).grid(
                        row=3, column=1,
                        padx=10, pady=20,
                        sticky=E
                        )


    # create function to accept details of other type of clean #
    def clean_check(self):

        if self.clean.get() == 'o':
            # create other clean frame
            self.other_clean = Toplevel(bg='#f9f5f0')
            self.other_clean.title('Specify Clean')

            ###LABELS###
            labels = (      ('Clean Description', 0, 0, 20), #name,row,column,padx
                            ('Charge', 0, 1, 0),
                            ('(€)', 1, 1, 0)
                            )
            for tup in labels:
                ttk.Label(
                            self.other_clean,
                            text=tup[0],
                            **self.label_settings
                    ).grid(
                            row=tup[1], column=tup[2],
                            padx=tup[3], pady=10,
                            sticky=W
                            )

            ###INPUTS###

            # create original in case of cancel
            self.clean_desc_original =    deepcopy(self.clean_desc.get())
            self.clean_charge_original =  deepcopy(self.clean_charge.get())

            clean_desc_entry = Entry(       self.other_clean,
                                            width=17,
                                            textvariable=
                                            self.clean_desc,
                                            font='Arial 11'
                                            )
            clean_desc_entry.grid(          row=1, column=0,
                                            padx=20, sticky=W
                                            )
            clean_chrg_entry = Entry(       self.other_clean,
                                            width=6,
                                            textvariable=
                                            self.clean_charge,
                                            font='Arial 11'
                                            )
            clean_chrg_entry.grid(          row=1, column=1,
                                            padx=30, sticky=W
                                            )

            #SAVE AND CANCEL#
            ttk.Button(
                            self.other_clean,
                            text='Save', width=5,
                            command=self.other_clean.destroy
                    ).grid(
                            row=3, column=1, padx=10, pady=10
                            )

            ttk.Button(
                            self.other_clean,
                            text='Cancel', width=7,
                            command=lambda: cancel(2)
                    ).grid(
                            row=3, column=0, columnspan=2, padx=10, pady=20
                            )


    # function to provide custom charge description #
    def custom_charge(self, id):

        # create pop-up window to take in custom charge description
        self.custom_window = Toplevel(  bg='#fbf9f6'            )

        if id == 3:
            self.custom_window.title(   'Custom Owner Charge'   )
        else:
            self.custom_window.title(   'Custom Guest Charge'   )

        # create label to ask for description
        ttk.Label(
                    self.custom_window,
                    text='Description',
                    background='#fbf9f6'
            ).grid(
                    row=0, column=0, padx=20, pady=10, sticky=W
                    )


        # decide which variable to use in the window
        if id == 3:
            # create copy of original in case of cancellation
            self.owner_original = deepcopy(self.custom_o_description.get())
            custom_var = self.custom_o_description
        else:
            self.guest_original = deepcopy(self.custom_g_description.get())
            custom_var = self.custom_g_description


        self.custom_description_entry = Entry(  self.custom_window,
                                                width=17,
                                                textvariable=
                                                custom_var,
                                                font='Arial 11'
                                                )
        self.custom_description_entry.grid(     row=1, column=0,
                                                padx=20,
                                                sticky=W
                                                )
        # SAVE and CANCEL buttons #
        ttk.Button(
                    self.custom_window,
                    text='Save',
                    width=5,
                    command=self.custom_window.destroy
            ).grid(
                    row=3, column=1, padx=10, pady=10
                    )

        ttk.Button(
                    self.custom_window,
                    text='Cancel',
                    width=7,
                    command=lambda: self.cancel(id)
            ).grid(
                    row=3, column=0, columnspan=2, padx=10, pady=20
                    )


    def edit_extras(self):


        if self.get_extras() == 'nnnn':
            messagebox.showerror('Nothing Selected', 'Select extras before editing')
            return

        self.extras_window = Toplevel(bg='#f9f5f0')
        self.extras_window.title('Edit Selected Extras')

        ##make copies of original values in case of cancellation##
        self.transfer_desc_original = deepcopy(self.transfer_desc.get())
        self.transfer_charge_original = deepcopy(self.transfer_charge.get())
        self.pack_desc_original = deepcopy(self.pack_desc.get())
        self.pack_charge_original = deepcopy(self.pack_charge.get())
        self.cotchair_desc_original = deepcopy(self.cotchair_desc.get())
        self.cotchair_charge_original = deepcopy(self.cotchair_charge.get())

        # call on function to provide list of standard settings
        list_of_tups = self.generate_extras_charges()

        column_count = 0
        for header in ('Item', 'Description', 'Charge'):
            Label(
                    self.extras_window,
                    text=header,
                    font='Lato 11 bold',
                    bg='#f9f5f0'
            ).grid(
                    row=0,
                    column=column_count,
                    padx=15,
                    pady=10,
                    sticky=W
            )
            column_count += 1


        row_count = 1
        for tup in list_of_tups:
            Label(
                    self.extras_window,
                    text=tup[0],
                    font='Lato 11',
                    bg='#f9f5f0'
            ).grid(
                    row=row_count,
                    column=0,
                    padx=15,
                    pady=5,
                    sticky=W
                    )
            desc_box = Entry(
                        self.extras_window,
                        width=18,
                        font='Arial 10',
                        textvariable=tup[2]
                        )
            desc_box.grid(
                        row=row_count,
                        column=1,
                        padx=15,
                        pady=5,
                        sticky=W
                        )
            charge_box = Entry(
                        self.extras_window,
                        width=6,
                        font='Arial 10',
                        textvariable=tup[1],
                        justify=RIGHT
                        )
            charge_box.grid(
                        row=row_count,
                        column=2,
                        padx=15,
                        pady=5,
                        sticky=W
                        )
            row_count += 1


        # SAVE and CANCEL buttons #
        ttk.Button(
                    self.extras_window,
                    text='Save',
                    width=5,
                    command=self.save_edits
            ).grid(
                    row=row_count, column=2, padx=10, pady=10
                    )

        ttk.Button(
                    self.extras_window,
                    text='Cancel',
                    width=7,
                    command=lambda: self.cancel(5)
            ).grid(
                    row=row_count, column=1, columnspan=2, padx=10, pady=20
                    )


    # checks for edits made to extras to keep for generating totals later #
    def save_edits(self):


        if (    self.transfer_desc.get() != self.transfer_desc_original.get()
            or
                self.transfer_charge.get() != self.transfer_charge_original.get()
        ):
            self.transfer_edited = True


        if (    self.pack_desc.get() != self.pack_desc_original.get()
            or
                self.pack_charge.get() != self.pack_charge_original.get()
        ):
            self.pack_edited = True


        if (    self.cotchair_desc.get() != self.cotchair_desc_original.get()
            or
                self.cotchair_charge.get() != self.cotchair_charge_original.get()
        ):
            self.cotchair_edited = True


        self.extras_window.destroy()


    # sets all variables back to the state before latest window pull
    def cancel(self, id):

        if id == 1:

            self.in_no.set(self.in_no_original)
            self.in_time.set(self.in_time_original)
            self.out_no.set(self.out_no_original)
            self.out_time.set(self.out_time_original)

            self.flight_window.destroy()

        if id == 2:

            self.clean_desc.set(self.clean_desc_original)
            self.clean_charge.set(self.clean_charge_original)

            self.other_clean.destroy()

        elif id == 3:

            self.custom_o_description.set(self.owner_original)
            self.custom_window.destroy()

        elif id == 4:

            self.custom_g_description.set(self.guest_original)
            self.custom_window.destroy()

        else:

            self.transfer_desc.set(self.transfer_desc_original)
            self.transfer_charge.set(self.transfer_charge_original)
            self.pack_desc.set(self.pack_desc_original)
            self.pack_charge.set(self.pack_charge_original)
            self.cotchair_desc.set(self.cotchair_desc_original)
            self.cotchair_charge.set(self.cotchair_charge_original)

            self.extras_window.destroy()




    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    ### RETURNER GET FUNCTIONS ###

    # returns a string of party numbers by age group 'ACB' and the integer total
    def get_party(self):
        party_str = (   self.adults.get()   +
                        self.kids.get()     +
                        self.babies.get()
                        )
        total = 0
        for char in party_str:
            total += int(char)
        return party_str, total


    # returns string of combined hours and minutes fields of eta selection
    def get_eta(self):
        return self.eta_hrs.get() + ':' + self.eta_mins.get()


    # function to return string of 'y' and 'n' concatenation in order of
    # extras selection. Order: Airport Transfer, Welcome Pack, Cot, High Chair
    def get_extras(self):
        extras_string = (   self.airport_transfer.get() +
                            self.welcome_pack.get()     +
                            self.cot.get()              +
                            self.high_chair.get()
                            )
        return extras_string




    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """......................................................................"""

    """CHECK SUBMISSION"""
    # function called when 'Generate Charges' button pressed
    def check_submission(self, update=False):


        # read and check if:
        ###     - property has been selected
        ###     - guest name has content
        ###     - total people is greater than 0
        ###     - arrival is before departure
        ###     - there is either flight time or eta
        ###     - if other clean selected ('o'), charge has been given

        # simplify variable names for the check
        arrival =       self.arrival.get()
        departure =     self.departure.get()


        ##Call on getters to make strins for ETA, Party composition, and extras
        ##these consolidate information and make iteration simpler
        self.party, self.total_people = self.get_party()
        self.eta =                      self.get_eta()
        self.extras_string =            self.get_extras()


        ##checking property##
        if self.property_selection.get() == 'Select from...':
            messagebox.showerror('No Property', 'Please select a property')
            return

        ##checking guest##
        if self.guest.get() == '':
            messagebox.showerror('No Name', 'Please enter guest name')
            return

        ##checking party##
        if self.total_people == 0:
            messagebox.showerror('No People', 'Please enter nº of guests')
            return


        ##checking dates##
        #check years
        if int(arrival[-4:]) > int(departure[-4:]):
            messagebox.showerror(   'Invalid Dates',
                                    'Arrival is after Departure'
                                    )
            return

        elif int(arrival[-4:]) == int(departure[-4:]):
            #check months
            if int(arrival[3:5]) > int(departure[3:5]):

                messagebox.showerror(   'Invalid Dates',
                                        'Arrival is after Departure'
                                        )
                return
            #check days
            elif int(arrival[3:5]) == int(departure[3:5]):

                if int(arrival[0:2]) > int(departure[0:2]):

                    messagebox.showerror(   'Invalid Dates',
                                            'Arrival is after Departure'
                                            )
                    return

                elif int(arrival[0:2]) == int(departure[0:2]):

                    messagebox.showerror(   'Invalid Dates',
                                            'Arrival is same as Departure'
                                            )
                    return


        #check transport and eta
        #get flight details from popup window if selected
        #check it has been created and in_time given
        if self.transport.get() == 'Flight':

            if self.in_time == '' and self.eta[0:2] == 'HH':
                messagebox.showerror(
                'No Inbound Time',
                '''Cannot calculate all fees without either Inbound Flight Time or ETA'''
                                        )
                return

        else:
            if self.eta[0:2] == 'HH':
                messagebox.showerror(   'No ETA',
                                        'Cannot calculate all fees without ETA'
                                        )
                return

        #check for other clean option
        #get description and charge from PopUp Class if selected, check charge
        if self.clean.get() == 'o':
            # instantiate object of the PopUp class for cleaning
            if self.o_clean_charge.get() == '':
                messagebox.showerror(   'No Charge',
                                        'Cannot calculate Other Clean without €'
                                        )
                return
            else:
                try:
                    float(self.o_clean_charge.get())
                except:
                    messagebox.showerror(   'Charge Error',
                                            'Cannot read given Other Clean charge'
                                            )
                    return


        if update == False:
            self.gen_charges.grid_remove()


        self.generate_charges()



    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """......................................................................"""
    """GENERATE CHARGES"""

    ##function to prepare tuples of extras charges##
    def generate_extras_charges(self):


        extras_string = self.get_extras()

        total_people =  self.get_party()[1]

        stay_length =   count_days(     self.arrival.get(),
                                        self.departure.get()
                                        )

        extras_charges_list = list()


        # check for airport transfer #
        if extras_string[0] == 'y':

            # if there has been an edit, keep those values
            if self.transfer_edited == True:
                pass

            else:
                # check for number of people and set charge accordingly
                if total_people <= 4:
                    charge = '79.00'
                elif total_people <= 8:
                    charge = '94.00'
                else:
                    charge ='173.00'

                self.transfer_desc.set('ret - ' + str(total_people) + ' pax')
                self.transfer_charge.set(charge)

            extras_charges_list.append(     ('Airport Transfer',
                                            self.transfer_charge,
                                            self.transfer_desc)
                                            )

        # check for welcome pack #
        if extras_string[1]== 'y':
            # always €30.00 and 'Standard'
            # will also keep edited values if edited
            extras_charges_list.append(     ('Welcome Pack',
                                            self.pack_charge,
                                            self.pack_desc)
                                            )

        # check for cot and high chair #
        # if either cot or high chair selected
        if extras_string[2] == 'y' or extras_string[3] == 'y':

            # set header despite any other conditions
            if extras_string[2:] == 'yy':
                header = 'Cot & High Chair'
            elif extras_string[2] == 'y':
                header = 'Cot'
            else:
                header = 'High Chair'

            # look for a previous edit that should not be overwritten
            if self.cotchair_edited == True:
                pass
            else:
                # find length of stay to set final rental price description
                if stay_length > 10:
                    self.cotchair_desc.set('Long Rental')
                else:
                    self.cotchair_desc.set('Short Rental')

                # if both cot and chair selected
                if extras_string[2:] == 'yy':

                    if stay_length > 10:
                        charge = '40.00'
                    else:
                        charge = '30.00'

                # if one or the other
                else:
                    if stay_length > 10:
                        charge = '30.00'
                    else:
                        charge = '20.00'

                self.cotchair_charge.set(charge)


            extras_charges_list.append(     (header,
                                            self.cotchair_charge,
                                            self.cotchair_desc)
                                            )

        return extras_charges_list


    # function called after the check of initial submission
    # check for pull from DB, standard is set to false
    def generate_charges(self, pull=False):

        #### OPTIONS ####
        ## Glossary:
            ## _settings = to set instantiation options
            ## _options = to set grid placement options
        # FRAME options
        frame_settings = {  'master': self.frame,
                            'padx': 9,
                            'pady': 15,
                            'bd': 5,
                            'bg': '#fbf9f6'
                            }
        frame_options = {   'padx': 10,
                            'pady': 15
                            }
        # SEPARATOR options
        separ_options = {   'column': 0,
                            'columnspan': 3,
                            'padx': 10,
                            'pady': 0,
                            'ipadx': 145
                            }
        # COLUMN options in cost listing
        lcol_settings = {   'font': 'Tlwg_Typist 10',
                            'background': '#fbf9f6'
                            }
        lcol_options = {    'column': 0,
                            'padx': 5,
                            'pady': 7,
                            'sticky': E
                            }
        mcol_settings = {   'width': 6,
                            'font': 'Arial 10',
                            'justify': RIGHT
                            }
        mcol_options = {    'column': 1,
                            'padx': 10,
                            'pady': 7
                            }
        rcol_settings = {   'font': 'Tlwg_Typist 9 italic',
                            'background': '#fbf9f6',
                            'foreground': '#333333'
                            }
        rcol_options = {    'column': 2,
                            'padx': 7,
                            'pady': 7,
                            'sticky': W
                            }
        # CUSTOM BUTTON options
        button_options = {  'width': 10,
                            'height': 1,
                            'fg': 'dark grey',
                            'font': 'Tlwg_Typist 8 italic',
                            'bg': '#f0f0f0'
                            }
        # options for TOTAL
        ltot_options = {    'column': 0,
                            'padx': 10,
                            'pady': 0,
                            'sticky': E
                            }


        ###FRAMES###
        # create charges frames after first submission
        self.owner_charges = LabelFrame(    **frame_settings
                                            )
        self.owner_charges.grid(            **frame_options,
                                            row=0,
                                            column=3
                                            )
        self.guest_charges = LabelFrame(    **frame_settings
                                            )
        self.guest_charges.grid(            row=1,
                                            **frame_options,
                                            column=3
                                            )


        # create TITLE labels
        titles = (  (self.owner_charges, 'Charges to Owner'),
                    (self.guest_charges, 'Charges to Guest')
                    )
        for tup in titles:
            Label(
                    tup[0],
                    text=tup[1],
                    bg='#fbf9f6',
                    font='Helvetica 13 bold'
            ).grid(
                    row=0, column=0, columnspan=3, padx=20, pady=20, sticky=N
                    )


        ####HEADERS####
        # create charges header labels and separator for both frames #
        # start with a loop for each frame
        for frame in (self.owner_charges, self.guest_charges):
            headers = ( ('Charge', 0, 5, E      ), #title,column,padx,sticky
                        ('Cost (€)', 1, 0, ''   ),
                        ('Details', 2, 5, W     )       )
            # proceed with a loop for each column header
            for tup in headers:
                ttk.Label(
                            frame,
                            text=tup[0],
                            font='Lato 11',
                            background='#fbf9f6'
                    ).grid(
                            row=1, column=tup[1],
                            padx=tup[2], pady=0,
                            sticky=tup[3]
                            )

            # add separator at end of inner loop to underline the column headers
            ttk.Separator(
                            frame,
                            orient='horizontal'
                    ).grid(
                            row=2, **separ_options
                            )



        """CALCULATING OWNER CHARGES"""
        # create owner charges breakdown #
        ###CHARGES###
        # Establish charge for CLEAN

        if pull == False:   # check for pull from DB

            ###CLEAN###
            clean = self.clean.get()

            if clean == 'y':
                clean_desc, clean_charge =          clean_calc(
                                                    self.name,
                                                    self.total_people
                                                    )

            elif clean == 'n':
                clean_desc =                        'No Clean'
                clean_charge =                      '0.00'

            else:
                pass


            ###MEET & GREET###
            if self.meetgreet.get() == 'y':
                meetgreet_desc =        'Standard'
                meetgreet_charge =      '25.00'

            else:
                meetgreet_desc =        'No Meet & Greet'
                meetgreet_charge =      '0.00'


        # create labels for the charges on owner side
        owner_charges_labels = (    ('Cleaning', 3      ),   # title, row
                                    ('Meet & Greet', 4  ),
                                    ('Custom Charge', 5 )
                                    )

        for tup in owner_charges_labels:
            ttk.Label(
                        self.owner_charges,
                        text=tup[0],
                        **lcol_settings
                ).grid(
                        row=tup[1],
                        **lcol_options
                        )


        # create BOXES to hold initial charges #
        if pull == False:
            self.clean_charge.set(clean_charge)
            self.clean_desc.set(clean_desc)
            self.meetgreet_charge.set(meetgreet_charge)
            self.meetgreet_desc.set(meetgreet_desc)

                                # variable, value, row
        owner_charges_boxes = ( (self.clean_charge, 3         ),
                                (self.meetgreet_charge, 4 ),
                                )

        for tup in owner_charges_boxes:
            box = Entry(    self.owner_charges,
                            textvariable=tup[0],
                            **mcol_settings
                            )
            box.grid(       row=tup[1],
                            **mcol_options
                            )

        # generate button and labels to show DETAILS of each charge
        owner_charges_details = (   (self.clean_desc, 3         ),  # value, row
                                    (self.meetgreet_desc, 4     ),
                                    (self.custom_owner_desc, 5  )
                                    )
        for tup in owner_charges_details:
            if tup[0] == self.custom_owner_desc:
                self.custom_owner_button = (
                        Button(
                                self.owner_charges,
                                textvariable=tup[0],
                                **button_options,
                                command=lambda: self.custom_charge(3)
                                )
                                )
                self.custom_owner_button.grid(  row=tup[1],
                                                **rcol_options
                                                )
            else:
                ttk.Label(
                            self.owner_charges,
                            textvariable=tup[0],
                            **rcol_settings
                    ).grid(
                            row=tup[1], **rcol_options
                            )

        ###OWNER CUSTOM###
        # create custom charge option
        self.custom_owner_label = ttk.Label(    self.owner_charges,
                                                text='Custom Charge',
                                                **lcol_settings
                                                )
        self.custom_owner_label.grid(           row=5,
                                                **lcol_options
                                                )
        self.custom_owner_entry = Entry(        self.owner_charges,
                                                textvariable=
                                                self.custom_owner_charge,
                                                **mcol_settings
                                                )
        self.custom_owner_entry.grid(           row=5,
                                                **mcol_options
                                                )


        """CALCULATING GUEST CHARGES"""
        # CONDITIONS FOR SETTING Charges
        # will determine which charges to apply and what tier
        # check for late meet and greet fee #
        # only when self.meetgreet is set to 'y'
        if pull == False:   # check for pull from DB

            if self.meetgreet.get() == 'y':

                late_meetgreet = False

                if self.transport.get() == 'Flight' and self.in_time.get() != '':

                    try:
                        if (    int(self.in_time.get()[0:2]) >= 18
                            or
                                int(self.in_time.get()[0:2]) <= 1
                        ):
                            late_meetgreet = True

                    except:
                        if (    int(self.in_time.get()[0:1]) <= 3
                            and
                                len(self.in_time.get()) == 4
                        ):
                            late_meetgreet = True

                else:
                    if (    int(self.eta[0:2]) >= 20
                        or
                            int(self.eta[0:2]) <= 3
                    ):
                        late_meetgreet = True


                if late_meetgreet == True:
                    self.list_guest_charges.append((    'Meet & Greet',
                                                        self.guest_meetgreet_charge,
                                                        self.guest_meetgreet_desc
                                                        ))

        # check for extras in self.extras string of 'y' and/or 'n' * 4
        # order is: airport transfer, welcome pack, cot, high chair
        # make exceptions for update vs new stay in database
        if pull == False:

            [self.list_guest_charges.append(tup) for tup in self.generate_extras_charges()]


        # place guest charges on the SCREEN #
        # number of guest charges varies according to time of arrival and
        # choice of extras
        # generate current row count for iteration
        self.row_count = 3

        if len(self.list_guest_charges) == 0:
            Label(      self.guest_charges,
                        text='There are no auto-generated charges'
                ).grid(
                        row=self.row_count, column=0, columnspan=3,
                        padx=5, pady=10
                        )
            self.row_count +=1
        else:
            for tup in self.list_guest_charges:
                ttk.Label(
                            self.guest_charges,
                            text=tup[0],
                            **lcol_settings
                    ).grid(
                            row=self.row_count,
                            **lcol_options
                            )

                self.charge_box = Entry(    self.guest_charges,
                                            textvariable=tup[1],
                                            **mcol_settings
                                            )
                self.charge_box.grid(       row=self.row_count,
                                            **mcol_options
                                            )

                ttk.Label(
                            self.guest_charges,
                            textvariable=tup[2],
                            **rcol_settings
                    ).grid(
                            row=self.row_count,
                            **rcol_options
                             )

                self.row_count +=1


        ###GUEST CUSTOM###
        # create custom charge option
        self.custom_guest_label = ttk.Label(    self.guest_charges,
                                                text='Custom Charge',
                                                **lcol_settings
                                                )
        self.custom_guest_label.grid(           row=self.row_count,
                                                **lcol_options
                                                )
        self.custom_guest_entry = Entry(        self.guest_charges,
                                                textvariable=
                                                self.custom_guest_charge,
                                                **mcol_settings
                                                )
        self.custom_guest_entry.grid(           row=self.row_count,
                                                **mcol_options
                                                )
        # create button for description option

        self.custom_guest_button = (
                            Button(
                                    self.guest_charges,
                                    textvariable=self.custom_guest_desc,
                                    **button_options,
                                    command=lambda: self.custom_charge(4)
                                    )
                                    )
        self.custom_guest_button.config(
                                            width=10, height=1
                                    )
        self.custom_guest_button.grid(      row=self.row_count, **rcol_options
                                    )


        ###Calculate TOTALS BUTTON###
        # create and palce generate totals button
        if pull == False:

            self.update_button_exists = False

            self.final_submission = Button(     self.frame,
                                                text='Submit',
                                                command=self.calculate_total,
                                                font='San_Francisco 11',
                                                background='white'
                                                )
            self.final_submission.grid(         row=2, column=2,
                                                columnspan=1,
                                                padx=20, pady=20, ipadx=20,
                                                sticky=S
                                                )
        else:

            self.update_button_exists = True

            self.update_button = Button(        self.frame,
                                                text='Update',
                                                command=self.update,
                                                font='San_Francisco 11',
                                                background='white'
                                                )
            self.update_button.grid(            row=2, column=2,
                                                columnspan=1,
                                                padx=20, pady=20, ipadx=20,
                                                sticky=S
                                                )

            self.calculate_total(pull=True)



    ### CALCULATE TOTAL FUNCTION ###
    def calculate_total(self, pull=False, update=False):

        ###OPTIONS###
        rcol_settings = {   'font': 'Tlwg_Typist 9 italic',
                            'background': '#fbf9f6',
                            'foreground': '#333333'
                            }
        rcol_options = {    'column': 2,
                            'padx': 7,
                            'pady': 7,
                            'sticky': W
                            }


        # wrap total calculation in a try/except statement to catch FLOAT
        # CONVERSION issues
        try:

            # gather and CALCULATE totals
            self.owner_total = (    float(self.clean_charge.get())          +
                                    float(self.meetgreet_charge.get())      +
                                    float(self.custom_owner_charge.get())
                                    )


            # check if custom charges given #
            # if yes, replace button with given description
            """
            if pull == False:

                if float(self.custom_owner_charge.get()) > 0.0:

                    self.custom_owner_button.config(

                                    text=self.custom_owner_desc.get()
                                    )

                if float(self.custom_guest_charge.get()) > 0.0:
                    if self.custom_g_description.get() != '':

                        self.custom_guest_button.config(

                                    text=self.custom_g_description.get()
                                    )

            """
            # determine how many guest charges there are #
            # get chrg_count from guest charges loop and use it
            self.guest_total = 0

            for n in range(0, len(self.list_guest_charges)):

                 self.guest_total += float(self.list_guest_charges[n][1].get())

            # add custom charge to guest final
            self.guest_total += float(self.custom_guest_charge.get())


            # create tuple for totals presentation
            totals = (  (self.owner_charges, 6, self.owner_total), # frame,row,variable
                        (self.guest_charges, self.row_count, self.guest_total)
                        )
            ##put totals on SCREEN##
            for tup in totals:
                # generate separator between rows of charges and total
                ttk.Separator(
                                tup[0],
                                orient='horizontal'
                        ).grid(
                                row=tup[1] + 1, column=0, columnspan=3,
                                padx=10, pady=0, ipadx=145
                                )
                # create a label 'TOTAL' to indicate final charge in left column
                ttk.Label(
                                tup[0],
                                text='TOTAL',
                                font='Tlwg_Typist 10',
                                background='#fbf9f6'
                        ).grid(
                                row=tup[1] + 2, column=0,
                                padx=10, pady=7, sticky=E
                                )
                # create label of total charge in middle column
                ttk.Label(
                                tup[0],
                                text='{:.2f}'.format(tup[2]),
                                background='#fbf9f6'
                        ).grid(
                                row=tup[1] + 2,
                                column=1,
                                padx=10,
                                pady=0
                                )

        except ValueError:
            messagebox.showerror(   'Invalid Values',
                                    'Check charges. Ensure format is "0.00".'
                                    )
            return


        if pull == True:
            pass
        elif update == False:
            #submit to database
            self.submit_to_db()
        else:
            self.update_db()


        # give update button option
        if self.update_button_exists == False:

            if pull == False:
                self.final_submission.grid_remove()
            else:
                pass

            self.update_button = Button(        self.frame,
                                                text='Update',
                                                command=self.update,
                                                font='San_Francisco 11',
                                                background='white'
                                                )
            self.update_button.grid(            row=2, column=2,
                                                columnspan=1,
                                                padx=20, pady=20, ipadx=20,
                                                sticky=S
                                                )




    def submit_to_db(self):


        # establish CONNECTION to database
        conn = sqlite3.connect('KKLJ.db')
        cur = conn.cursor()


        # get property id from Properties table in DB
        cur.execute(    'SELECT id FROM Properties WHERE name=?',
                        (self.name,)
                        )
        property_id =   cur.fetchone()[0]


        # push guest detail into Guest table, then pull id for Stay table
        cur.execute(    'INSERT OR IGNORE INTO Guests (name, email) VALUES (?, ?)',
                        (self.guest.get(), self.email.get())
                        )
        cur.execute(    'SELECT id FROM Guests WHERE email=?',
                        (self.email.get(),)
                        )
        self.guest_id = cur.fetchone()[0]

        # push first details to Stay table, get stay id
        cur.execute(''' INSERT INTO Stay
                        (   prop_id, guest_id, arrival,
                            departure, party_size, security, owner
                            )
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?
                        )''',
                        (   property_id, self.guest_id, self.arrival.get(),
                            self.departure.get(), self.party, self.security.get(),
                            self.owner.get()
                            )
                        )
        cur.execute(    'SELECT id FROM Stay WHERE prop_id=? AND arrival=?',
                        (property_id, self.arrival.get())
                        )
        self.id = cur.fetchone()[0]


        # push transport information to Transport table
        # create variables for flight details
        if self.transport.get() == 'Flight':
            in_no =     self.in_no.get()
            in_time =   self.in_time.get()
            out_no =    self.out_no.get()
            out_time =  self.out_time.get()
        else:
            in_no =     'n/a'
            in_time =   'n/a'
            out_no =    'n/a'
            out_time =  'n/a'
        cur.execute(''' INSERT INTO Transport
                        (   stay_id, transport, carhire, eta,
                            f_in_no, f_in_time, f_out_no, f_out_time
                            )
                        VALUES
                        (   ?,?,?,?,?,?,?,?
                            )
                        ''',
                        (   self.id, self.transport.get(), self.carhire.get(),
                            self.eta, in_no, in_time, out_no, out_time
                            )
                        )


        # push CHARGES to OWNER to Charges_Owner table in DB
        # make strings to consolidate information, using ';' to separate type
        ###CLEAN###
        clean = (
                        self.clean.get()        +
                        ';'                     +
                        self.clean_charge.get() +
                        ';'                     +
                        self.clean_desc.get()
                        )

        ###MEET & GREET###
        meetgreet = (
                        self.meetgreet.get()        +
                        ';'                         +
                        self.meetgreet_charge.get() +
                        ';'                         +
                        self.meetgreet_desc.get()
                        )

        ###CUSTOM###
        custom_owner = (
                        self.custom_owner_charge.get()  +
                        ';'                             +
                        self.custom_owner_desc.get()
                        )

        ###TOTAL###
        owner_total = '{:.2f}'.format(self.owner_total)

        cur.execute(''' INSERT INTO Charges_Owner
                        (stay_id, prop_id, clean, meetgreet, custom, total)
                        VALUES
                        (?,?,?,?,?,?)
                        ''',
                        (   self.id, property_id, clean,
                            meetgreet, custom_owner, owner_total
                            )
                        )


        # push CHARGES to GUEST to Charges_Guest table in DB
        # make strings to consolidate information, using ';' to separate type
        # call on list_guest_charges to fill out details of extras selected
        # set variables to push to negative and change if found in list
        meetgreet_fee = 'n'
        airport_transfer = 'n'
        welcome_pack = 'n'
        cot_highchair = 'nn'

        for tup in self.list_guest_charges:

            if tup[0] == 'Meet & Greet':
                meetgreet_fee = 'y;' + tup[1].get() + ';' + tup[2].get()
            elif tup[0] == 'Airport Transfer':
                airport_transfer = 'y;' + tup[1].get() + ';' + tup[2].get()
            elif tup[0] == 'Welcome Pack':
                welcome_pack = 'y;' + tup[1].get() + ';' + tup[2].get()
            else:
                cot_highchair = (   self.extras_string[2]   +
                                    self.extras_string[3]   +
                                    ';'                     +
                                    tup[1].get()            +
                                    ';'                     +
                                    tup[2].get()
                                    )

        custom_guest = (    self.custom_guest_charge.get()  +
                            ';'                             +
                            self.custom_guest_desc.get()
                            )

        guest_total = '{:.2f}'.format(self.guest_total)

        cur.execute(''' INSERT INTO Charges_Guest
                        (   stay_id, meetgreet, transfer, pack,
                            cot_chair, custom, total
                            )
                        VALUES
                        (   ?,?,?,?,?,?,?
                            )''',
                        (   self.id, meetgreet_fee, airport_transfer,
                            welcome_pack, cot_highchair, custom_guest,
                            guest_total
                            )
                        )

        conn.commit()
        conn.close()





    def update(self):

        self.owner_charges.grid_remove()
        self.guest_charges.grid_remove()

        self.list_guest_charges.clear()

        self.check_submission(update=True)
        self.calculate_total(update=True)
        self.update_db()




    def update_db(self):


        conn = sqlite3.connect('KKLJ.db')
        cur = conn.cursor()

        # get property id from Properties table in DB
        cur.execute(    'SELECT id FROM Properties WHERE name=?',
                        (self.name,)
                        )
        property_id =   cur.fetchone()[0]


        # push guest detail into Guest table, then pull id for Stay table
        cur.execute(    'UPDATE Guests SET name = ?, email = ? WHERE id = ?',
                        (self.guest.get(), self.email.get(), self.guest_id)
                        )


        # push first details to Stay table, get stay id
        cur.execute(''' UPDATE  Stay
                        SET     prop_id = ?, arrival = ?, departure = ?,
                                party_size = ?, security = ?,
                                owner = ?
                        WHERE   id = ?''',
                        (       property_id, self.arrival.get(),
                                self.departure.get(), self.party,
                                self.security.get(), self.owner.get(),
                                self.id
                                )
                        )


        # push transport information to Transport table
        # create variables for flight details
        if self.transport.get() == 'Flight' and self.flight_info == 'y':
            in_no =     self.in_no.get()
            in_time =   self.in_time.get()
            out_no =    self.out_no.get()
            out_time =  self.out_time.get()
        else:
            in_no =     'n/a'
            in_time =   'n/a'
            out_no =    'n/a'
            out_time =  'n/a'
        cur.execute(''' UPDATE  Transport
                        SET     transport = ?, carhire = ?, eta = ?,
                                f_in_no = ?, f_in_time = ?,
                                f_out_no = ?, f_out_time = ?
                        WHERE   stay_id = ?''',
                        (       self.transport.get(), self.carhire.get(),
                                self.eta, in_no, in_time, out_no, out_time,
                                self.id
                                )
                        )


        # push CHARGES to OWNER to Charges_Owner table in DB
        # make strings to consolidate information, using ';' to separate type
        ###CLEAN###
        clean = (   self.clean.get()        +
                    ';'                     +
                    self.clean_charge.get() +
                    ';'                     +
                    self.clean_desc.get()
                        )

        ###MEET & GREET###
        meetgreet = (
                        self.meetgreet.get()        +
                        ';'                         +
                        self.meetgreet_charge.get() +
                        ';'                         +
                        self.meetgreet_desc.get()
                        )

        ###CUSTOM###
        custom_owner = (
                            self.custom_owner_charge.get()  +
                            ';'                             +
                            self.custom_owner_desc.get()
                            )

        ###TOTAL###
        owner_total = '{:.2f}'.format(self.owner_total)

        cur.execute(''' UPDATE  Charges_Owner
                        SET     prop_id = ?, clean = ?, meetgreet = ?,
                                custom = ?, total = ?
                        WHERE   stay_id = ?''',
                        (       property_id, clean, meetgreet,
                                custom_owner, owner_total,
                                self.id
                                )
                        )


        # push CHARGES to GUEST to Charges_Guest table in DB
        # make strings to consolidate information, using ';' to separate type
        # call on list_guest_charges to fill out details of extras selected
        # set variables to push to negative and change if found in list
        meetgreet_fee = 'n'
        airport_transfer = 'n'
        welcome_pack = 'n'
        cot_highchair = 'nn'

        for tup in self.list_guest_charges:

            if tup[0] == 'Meet & Greet':
                meetgreet_fee = 'y;' + tup[1].get() + ';' + tup[2].get()
            elif tup[0] == 'Airport Transfer':
                airport_transfer = 'y;' + tup[1].get() + ';' + tup[2].get()
            elif tup[0] == 'Welcome Pack':
                welcome_pack = 'y;' + tup[1].get() + ';' + tup[2].get()
            else:
                cot_highchair = (   self.extras_string[2]   +
                                    self.extras_string[3]   +
                                    ';'                     +
                                    tup[1].get()            +
                                    ';'                     +
                                    tup[2].get()
                                    )

        custom_guest = (    self.custom_guest_charge.get()  +
                            ';'                             +
                            self.custom_guest_desc.get()
                            )

        guest_total = '{:.2f}'.format(self.guest_total)

        cur.execute(''' UPDATE  Charges_Guest
                        SET     meetgreet = ?, transfer = ?, pack = ?,
                                cot_chair = ?, custom = ?, total = ?
                        WHERE   stay_id = ?''',
                        (       meetgreet_fee, airport_transfer, welcome_pack,
                                cot_highchair, custom_guest, guest_total,
                                self.id
                                )
                        )


        conn.commit()
        conn.close()



    def database_pull(self):


        conn = sqlite3.connect('KKLJ.db')
        cur = conn.cursor()


        cur.execute(''' SELECT      prop_id, guest_id, arrival,
                                    departure, party_size, security, owner
                        FROM Stay
                        WHERE id=?''', (self.id,)
                        )

        (   prop_id, self.guest_id, arrival,
            departure, party, security, owner   ) = cur.fetchall()[0]


        cur.execute(''' SELECT      name, email
                        FROM Guests
                        WHERE id=?''', (self.guest_id,)
                        )
        guest_name, guest_email = cur.fetchall()[0]


        cur.execute(''' SELECT      name
                        FROM Properties
                        WHERE id=?''', (prop_id,)
                        )
        prop_name = cur.fetchone()[0]


        for prop in self.lst:
            if prop[-6:] == prop_name[-6:]:
                self.name = prop
                break
        self.owner.set(owner)
        self.guest.set(guest_name)
        self.email.set(guest_email)

        self.adults.set(party[0])
        self.kids.set(party[1])
        self.babies.set(party[2])

        self.arrival_date =     arrival
        self.departure_date =   departure

        self.security.set(security)


        cur.execute(''' SELECT  transport, carhire, eta,
                                f_in_no, f_in_time, f_out_no, f_out_time
                        FROM Transport
                        WHERE stay_id=?''', (self.id,)
                        )
        (   transport, carhire, eta,
            f_in_no, f_in_time, f_out_no, f_out_time    ) = cur.fetchall()[0]


        self.transport.set(transport)
        self.carhire.set(carhire)
        self.eta_hrs.set(eta[:2])
        self.eta_mins.set(eta[3:])

        if transport == 'Flight':

            if f_in_no != 'n/a':
                self.in_no.set(f_in_no)
            else:
                self.in_no.set('')

            if f_in_time != 'n/a':
                self.in_time.set(f_in_time)
            else:
                self.in_time.set('')

            if f_out_no != 'n/a':
                self.out_no.set(f_out_no)
            else:
                self.out_no.set('')

            if f_out_time != 'n/a':
                self.out_time.set(f_out_time)
            else:
                self.out_time.set('')

        else:
            self.in_no.set('')
            self.in_time.set('')
            self.out_no.set('')
            self.out_time.set('')


        cur.execute(''' SELECT      clean, meetgreet, custom
                        FROM Charges_Owner
                        WHERE stay_id=?''', (self.id,)
                        )
        clean, meetgreet, custom_owner = cur.fetchall()[0]


        clean_list = clean.split(';')
        meetgreet_list = meetgreet.split(';')
        custom_owner_list = custom_owner.split(';')

        ## OWNER CUSTOM ##
        try:
            self.custom_owner_charge.set(custom_owner_list[0])
            self.custom_owner_desc.set(custom_owner_list[1])
        except:
            self.custom_owner_charge.set('0.00')
            self.custom_owner_desc.set('Add description')

        ###MANAGEMENT VARS###
        self.clean.set(clean_list[0])
        self.clean_charge.set(clean_list[1])
        self.clean_desc.set(clean_list[2])

        self.meetgreet.set(meetgreet_list[0])
        self.meetgreet_charge.set(meetgreet_list[1])
        self.meetgreet_desc.set(meetgreet_list[2])


        cur.execute(''' SELECT      meetgreet, transfer, pack, cot_chair, custom
                        FROM Charges_Guest
                        WHERE stay_id=?''', (self.id,)
                        )
        guest_greet, transfer, pack, cot_chair, custom_guest = cur.fetchall()[0]


        ###GUEST CHARGES AND EXTRAS VARS###
        if guest_greet != 'n':
            guest_greet_list = guest_greet.split(';')
            self.guest_meetgreet_charge.set(guest_greet_list[1])
            self.guest_meetgreet_desc.set(guest_greet_list[2])
            self.list_guest_charges.append(
                                            ('Meet & Greet',
                                            self.guest_meetgreet,
                                            self.guest_meetgreet_desc)
                                            )
        else:
            self.guest_meetgreet_charge.set('20.00')
            self.guest_meetgreet_desc.set('Late fee')


        if transfer != 'n':
            transfer_list = transfer.split(';')
            self.airport_transfer.set('y')
            self.transfer_charge.set(transfer_list[1])
            self.transfer_desc.set(transfer_list[2])
            self.list_guest_charges.append(
                                            ('Airport Transfer',
                                            self.transfer_charge,
                                            self.transfer_desc)
                                            )
        else:
            self.airport_transfer.set('n')


        if pack != 'n':
            pack_list = pack.split(';')
            self.welcome_pack.set('y')
            self.pack_charge.set(pack_list[1])
            self.pack_desc.set(pack_list[2])
            self.list_guest_charges.append(
                                            ('Welcome Pack',
                                            self.pack_charge,
                                            self.pack_desc)
                                            )
        else:
            self.welcome_pack.set('n')
            self.pack_charge.set('30.00')
            self.pack_desc.set('Standard')


        if cot_chair != 'nn':
            cot_chair_list = cot_chair.split(';')
            self.cot.set(cot_chair_list[0][0])
            self.high_chair.set(cot_chair_list[0][1])
            self.cotchair_charge.set(cot_chair_list[1])
            self.cotchair_desc.set(cot_chair_list[2])
            if cot_chair_list[0] == 'yn':
                text = 'Cot'
            elif cot_chair_list[0] == 'ny':
                text = 'High Chair'
            else:
                text = 'Cot & High Chair'
            self.list_guest_charges.append(
                                            (text,
                                            self.cot_chair_charge,
                                            self.cotchair_desc)
                                            )
        else:
            self.cot.set('n')
            self.high_chair.set('n')


        try:
            custom_guest_list = custom_guest.split(';')
            self.custom_guest_charge.set(custom_guest_list[0])
            self.custom_guest_desc.set(custom_guest_list[1])
        except:
            self.custom_guest_charge.set('0.00')
            self.custom_guest_desc.set('Add description')




    def destroy_frames(self):

        try:
            self.first.grid_remove()
            self.second.grid_remove()
            self.extras.grid_remove()
            self.management.grid_remove()
            self.owner_charges.grid_remove()
            self.guest_charges.grid_remove()
        except:
            self.first.grid_remove()
            self.second.grid_remove()
            self.extras.grid_remove()
            self.management.grid_remove()

        try:
            self.gen_charges.grid_remove()
        except:
            try:
                self.final_submission.grid_remove()
            except:
                self.update_button.grid_remove()
