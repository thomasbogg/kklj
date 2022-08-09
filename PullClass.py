from tkinter import *
from tkinter import messagebox, ttk, Text, font
from tkcalendar import Calendar, DateEntry
from functions import set_date,  between_dates
from StayClass import Stay
import sqlite3
from datetime import date



class Pull:

    cal_settings = {    'selectmode': 'day',
                        'locale': 'en_UK',
                        'font': 'Arial 11',
                        'showweeknumbers': False,
                        'showothermonthdays': False,
                        'weekendbackground': '#ededed',
                        'weekendforeground': 'black',
                        'width': 12
                        }

    space_settings = {  'padx': 5,
                        'pady': 15}

    def __init__(self, frame, type):

        self.frame = frame
        self.type = type

        self.header =   LabelFrame(     self.frame,
                                        padx=15,
                                        pady=15,
                                        background='#f9f5f0'
                                        )
        self.header.grid(               row=0,
                                        column=1,
                                        padx=20,
                                        pady=20,
                                        sticky=N)



        # initiate a property list to set in drop down menu in header frame for search
        prop_list = ['All properties...']

        # call on func in Stay class to produce list from DataBase
        props = Stay.build_prop_list(self, type='pull')

        # iterate through returned list to populate 'prop_list'
        for prop in props:
            prop_list.append(prop)

        self.property = StringVar()

        prop_box = ttk.Combobox(    self.header,
                                    textvariable=self.property,
                                    values=prop_list,
                                    font='Arial 11',
                                    width=22,
                                    state='readonly'
                                    )
        prop_box.grid(              row=0,
                                    column=1,
                                    columnspan=3,
                                    **self.space_settings,
                                    sticky=W
                                    )

        if self.type == 'stay':
            heading_prop = 'Search STAYS in'
            heading_from = '...starting between'
        else:
            heading_prop = 'Search CLEANS in'
            heading_from = '...ending between'


        self.property.set('All properties...')


        self.heading_prop =     Label(  self.header,
                                        text=heading_prop,
                                        font='Helvetica 13',
                                        bg='#f9f5f0'
                                        )
        self.heading_from =     Label(  self.header,
                                        text=heading_from,
                                        font='Helvetica 13',
                                        bg='#f9f5f0'
                                        )
        self.heading_to =       Label(  self.header,
                                        text='and',
                                        font='Helvetica 13',
                                        bg='#f9f5f0'
                                        )
        self.heading_prop.grid(         row=0,
                                        column=0,
                                        columnspan=1,
                                        **self.space_settings,
                                        sticky=W
                                        )
        self.heading_from.grid(         row=1,
                                        column=0,
                                        columnspan=1,
                                        **self.space_settings,
                                        sticky=W
                                        )
        self.heading_to.grid(           row=1,
                                        column=2,
                                        columnspan=1,
                                        **self.space_settings
                                        )

        self.start_date =   StringVar()
        self.end_date =     StringVar()

        start_label =       Label(self.header)

        self.start_cal =    DateEntry(  self.header,
                                        textvariable=self.start_date,
                                        **self.cal_settings
                                        )
        self.start_cal.grid(            row=1,
                                        column=1,
                                        **self.space_settings
                                        )
        self.end_cal =      DateEntry(  self.header,
                                        textvariable=self.end_date,
                                        **self.cal_settings
                                        )
        self.end_cal.grid(              row=1,
                                        column=3,
                                        **self.space_settings,
                                        sticky=E
                                        )

        if self.type == 'stay':
            first_date =    date.today().strftime('%d/%m/%Y')
            last_date =     set_date(date.today().strftime('%d/%m/%Y'), 'e')
        else:
            first_date =    set_date(date.today().strftime('%d/%m/%Y'), '-5')
            last_date =     date.today().strftime('%d/%m/%Y')


        self.start_date.set(first_date)
        self.end_date.set(last_date)


        self.submit_button()

        self.stay_pulled = False
        self.clean_pulled = False

        self.pull_from_db()




    def pull_from_db(self, again=False):


        # check for renewed search
        if again == True:
            self.results.destroy()


        self.results = LabelFrame(self.frame, padx=20, pady=20)
        self.results.grid(row=1, column=1, padx=20, pady=10)


        conn = sqlite3.connect('KKLJ.db')
        cur = conn.cursor()

        # set simple variable for easier iteration
        property = self.property.get()

        # check for property choice
        if property != 'All properties...':

            cur.execute('SELECT id FROM Properties WHERE name=?', (property,))
            prop_id = cur.fetchone()[0]

        else: pass


        dates_list = between_dates(self.start_date.get(), self.end_date.get())

        listed_stay_ids = list()


        row_count = 0
        for date in dates_list:

            if property != 'All properties...':

                if type == 'stay':

                    cur.execute(''' SELECT      id, prop_id, guest_id,
                                                arrival, departure
                                    FROM Stay
                                    WHERE arrival=? AND prop_id=?''',
                                    (date, prop_id)
                                    )

                else:
                    cur.execute(''' SELECT      id, prop_id, guest_id,
                                                arrival, departure
                                    FROM Stay
                                    WHERE departure=? AND prop_id=?''',
                                    (date, prop_id)
                                    )

            else:
                if self.type == 'stay':
                    cur.execute(''' SELECT      id, prop_id, guest_id,
                                                arrival, departure
                                    FROM Stay
                                    WHERE arrival=?''',
                                    (date,)
                                    )
                else:
                    cur.execute(''' SELECT      id, prop_id, guest_id,
                                                arrival, departure
                                    FROM Stay
                                    WHERE departure=?''',
                                    (date,)
                                    )

            fetched = cur.fetchall()

            for tup in fetched:

                stay_id, prop_id, guest_id, arrival, departure = tup

                listed_stay_ids.append(stay_id)

                cur.execute('SELECT name FROM Properties WHERE id=?', (prop_id,))
                prop_name = cur.fetchone()[0]

                cur.execute('SELECT name FROM Guests WHERE id=?', (guest_id,))
                guest_name = cur.fetchone()[0]

                column_count = 0

                if self.type == 'stay':
                    items = (guest_name, prop_name, arrival, departure)
                else:
                    items = (guest_name, prop_name, departure)

                for item in items:

                    if column_count == 0 or column_count == 1:
                        stick = W
                    else:
                        stick = ''

                    Label(
                            self.results,
                            text=item
                    ).grid(
                            row=row_count,
                            column=column_count,
                            padx=4,
                            pady=2,
                            sticky=stick)

                    column_count += 1

                row_count += 1


            button_dict = dict()
            row_count = 0

            for id in listed_stay_ids:

                def func(x=id):
                    if self.type == 'stay':
                        return self.throw_pull(x)
                    else:
                        return self.throw_clean(x)

                button_dict[id] = Button(
                                            self.results,
                                            text='Details',
                                            command=func
                )
                button_dict[id].grid(
                                            row=row_count,
                                            column=4,
                                            padx=4,
                                            pady=3
                )
                row_count +=1



        conn.commit()
        conn.close()


        self.submit_button(again=True)



    def throw_pull(self, id):

        self.destroy_frames()

        self.stay_pulled = True

        self.throw = Stay(self.frame, 'old', id)



    def throw_clean(self, id):

        self.destroy_frames()

        self.clean_pulled = True

        self.clean = LabelFrame(    self.frame,
                                    padx=20,
                                    pady=20
                                    )
        self.clean.grid(    row=0, column=1)



    def submit_button(self, again=False):


        self.submit =       Button( self.header,
                                    text='Submit',
                                    font='San_Francisco 11',
                                    background='white',
                                    command=lambda: self.pull_from_db(again=True)
                                    )

        self.submit.grid(           row=2,
                                    column=0,
                                    columnspan=4,
                                    **self.space_settings
                                    )


    def destroy_frames(self):

        try:
            self.header.grid_remove()
            self.results.grid_remove()
        except:
            self.header.grid_remove()
