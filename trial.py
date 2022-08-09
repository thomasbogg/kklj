from tkinter import *
from tkinter import messagebox, ttk, Text, font
from tkcalendar import Calendar, DateEntry
import functions as F
import classes as C


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('KKLJ Property Management Software BETA')
        #width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        #self.geometry('%dx%d+0+0' % (width, height))
        self.geometry('1000x800')
        self.configure(bg='#efe5d9')

        # create Stay Frame
        stay_frame = LabelFrame(self)
        stay_frame.grid(row=0, column=0)

        # define universal styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', font=('Nexa', '10'), background='white'    )
        self.option_add('*TCombobox*Listbox.font', ('Nexa', '10')               )
        style.configure('TLabel', font='Nexa 10', background='#f9f5f0'          )
        style.configure('TEntry', font='Arial 10'                               )
        style.configure('TRadiobutton', font='Arial 10', background='#f9f5f0'   )
        style.configure('TCheckbutton', font='Nexa 10', background='#f9f5f0'    )
        style.configure('TButton', font='San_Francisco 9', background='white'  )


class Stay(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        #### OPTIONS ####
        ## Glossary:
            ## _settings = to set instantiation options
            ## _options = to set grid placement options
        self.frame_settings = { 'master': container,
                                'bd': 5,
                                'bg': '#f9f5f0'                 }
        self.title_settings = { 'font': 'Helvetica 14 bold',
                                'bg': '#f9f5f0'                 }
        self.title_options = {  'row': 0,
                                'column': 0,
                                'columnspan': 2,
                                'pady': 15,
                                'sticky': N                     }




        # initialise all three starting frames
        self.generate_frames()


    def generate_frames(self):

        # create 3 frames
        self.main =         LabelFrame(**self.frame_settings, padx=24, pady=25)
        self.management =   LabelFrame(**self.frame_settings, padx=28, pady=32)
        self.extras =       LabelFrame(**self.frame_settings, padx=25, pady=32)
        # put them on grid
        frames = (  (self.main, 0, N        ),  # name, column, sticker
                    (self.management, 1, N  ),
                    (self.extras, 1, S      )   )
        for tup in frames:
            tup[0].grid(row=0, column=tup[1], padx=10, pady=10, sticky=tup[2])


        # call on functions to populate frames
        self.main_frame()
        #self.management_frame()
        #self.extras_frame()

        ###GENERATE CHARGES###
        # create and palce generate charges button
        self.gen_charges = Button(  self.container,
                                    text='Generate Charges',
                                    #command=self.check_submission,
                                    font='San_Francisco 11',
                                    background='white'              )
        self.gen_charges.grid(
                                    row=1, column=0,
                                    columnspan=2,
                                    padx=20, pady=20, ipadx=20,
                                    sticky=S                        )

    def main_frame(self):
        #### OPTIONS ####
        ## Glossary:
            ## _settings = to set instantiation options
            ## _options = to set grid placement options
        radioY_settings = { 'text': 'Yes',
                            'value': 'y'                    }
        radioN_settings = { 'text': 'No',
                            'value': 'n'                    }
        radio_options = {   'column': 1,
                            'padx': 21                      }
        cal_settings = {    'selectmode': 'day',
                            'locale': 'en_UK',
                            'font': 'Arial 10',
                            'showweeknumbers': False,
                            'showothermonthdays': False,
                            'weekendbackground': '#ededed',
                            'weekendforeground': 'black',
                            'width': 12                     }
        """
        # call on Property class for generation and interactivity of first 2 rows
        self.property = C.HeadProperty(self.main)

        #####LABELS####
        # create labels of column 0 of Main Frame and place on grid
        main_labels = ( 'Owner',
                        'Guest',
                        'Email',
                        'Party Composition',
                        'Arriving',
                        'Departing',
                        'Transportation',
                        'Hiring a Car',
                        'ETA'               )
        row_count = 2 # starting count for row num to loop
        for item in main_labels:
            # skip party comp row, will use frame instead
            if item == 'Party Composition':
                row_count += 1
            else:
                ttk.Label(  self.main,
                            text=item   ).grid( row=row_count, column=0,
                                                padx=20, pady=10,
                                                sticky=W                    )
                row_count += 1

        # create radio button for owner #
        self.owner_selection =  StringVar(self.main, 'n')
        #self.owner_selection.set('n')
        owner_yes = ttk.Radiobutton(    self.main,
                                        **radioY_settings,
                                        variable=self.owner_selection       )
        owner_yes.grid(                 row=2, **radio_options, sticky=W    )

        owner_no = ttk.Radiobutton(     self.main,
                                        **radioN_settings,
                                        variable=self.owner_selection       )
        owner_no.grid(                  row=2, **radio_options, sticky=E    )

        #####FIELDS####
        # guest NAME and EMAIL text fields, on rows 3 and 4
        self.name =     StringVar(self.main, ' ')
        self.email =    StringVar(self.main, ' ')

        name_email = (  (self.name, 3   ),      # variable, row
                        (self.email, 4  )           )

        for tup in name_email:
            field = Entry(  self.main,
                            textvariable=tup[0],
                            width=22,
                            font='Arial 10'         )
            field.grid(     row=tup[1], column=0,
                            columnspan=2,
                            padx=20, pady=0,
                            sticky=E                )

        """

        # create internal frame for party composition labels fields #
        # initiate frame
        self.party_frame = LabelFrame(   self.main,
                                    padx=10, pady=0,
                                    bd=0, bg='#f9f5f0'  )
        self.party_frame.grid(
                                    row=5, column=0,
                                    columnspan=2,
                                    padx=10, pady=10,
                                    sticky=W            )

        # create conditions for loop placement of labels/fields in frame
        # initialise variable to hold input
        self.adults =   StringVar(self.party_frame, '2')
        self.kids = StringVar(self.party_frame, '0')
        self.babies =   StringVar(self.party_frame, '0')


        party_labels = (    ('Adults', self.adults),
                            ('   ', ''),
                            ('Children', self.kids),
                            ('   ', ''),
                            ( 'Babies', self.babies)   )

        for tup in party_labels:

            ttk.Label(self.party_frame, text=tup[0]).pack(side=LEFT)

            if tup[0] != '   ':
                field = Entry(  self.party_frame,
                                textvariable=tup[1],
                                width=2,
                                justify=RIGHT,
                                font='Arial 10', bg='#EBECF0'   )
                field.pack(side=LEFT)

        """
        # setting arrival and departure dates #
        # declare string variables for dates
        self.arrival_str =   StringVar()
        self.departure_str = StringVar()

        # labels for the calendar inputs
        # initialise and place arrival and departure calendars
        arrival_date = DateEntry(   self.main,
                                    textvariable=self.arrival_str,
                                    **cal_settings                  )
        arrival_date.grid(          row=6, column=1                 )

        departure_date = DateEntry( self.main,
                                    textvariable=self.departure_str,
                                    **cal_settings                  )
        departure_date.grid(        row=7, column=1                 )

        # create a check for mode of transportation #
        # use a list to prepare items to display in dropdown
        transport_items = [
                            'Flight',
                            'Car',
                            'Train',
                            'Bus'
        ]

        # set variable to hold selection
        self.transport_selection = StringVar(self.main, 'Coming by...')

        #self.transport_selection.set('Coming by...')
        # call on PopUp class to check whether flight details window is necessary
        # will take flights from the PopUp class get_flights() fucntion
        self.t_option = C.PopUp(self.transport_selection, 'T')

        transport_field = OptionMenu(   self.main,
                                        self.transport_selection,
                                        *transport_items,
                                        command=self.t_option.transport_check   )
        transport_field.config(
                                        width=10, font='Arial 10', bg='white',
                                        anchor=W, borderwidth=0                 )
        transport_field.grid(
                                        row=8, column=1, padx=20, pady=0        )

        # create radio button and variable for car hire #
        self.carhire_selection = StringVar(self.main, 'n')
        #self.carhire_selection.set('n')
        carhire_yes = ttk.Radiobutton(  self.main,
                                        **radioY_settings,
                                        variable=self.carhire_selection     )
        carhire_yes.grid(               row=9, **radio_options, sticky=W    )

        carhire_no = ttk.Radiobutton(   self.main,
                                        **radioN_settings,
                                        variable=self.carhire_selection     )
        carhire_no.grid(                row=9, **radio_options, sticky=E    )

        # create dropdown for hours and mins for ETA declaration #
        # use combobox for better scrolling
        self.eta_hrs = ttk.Combobox( self.main, font='Arial 10',
                                state='readonly', width=3               )
        self.eta_hrs['values'] = (   'HH', '00', '01', '02', '03', '04', '05', '06',
                                '07', '08', '09', '10', '11', '12', '13', '14',
                                '15', '16', '17', '18', '19', '20', '21', '22',
                                '23'                                    )
        self.eta_hrs.set('HH')
        self.eta_hrs.grid(   row=10, column=1, padx=20, sticky=W        )

        self.eta_mins = ttk.Combobox(   self.main, font='Arial 10',
                                        state='readonly', width=3       )
        self.eta_mins['values'] = ['MM', '00', '15', '30', '45']
        self.eta_mins.set('MM')
        self.eta_mins.grid(  row=10, column=1, padx=20, sticky=E        )
        """

if __name__ == '__main__':
    app = App()
    Stay(app)
    app.mainloop()
