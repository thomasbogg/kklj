from tkinter import *
from tkinter import messagebox, ttk, Text, font
from StayClass import Stay
from PullClass import Pull
import sqlite3



class App(Tk):

    def __init__(self):
        super().__init__()

        self.title('KKLJ Property Management Software BETA')
        #width, height = self.winfo_screenwidth(), self.winfo_screenheight()
        #self.geometry('%dx%d+0+0' % (width, height))
        #self.geometry('1000x800')
        self.configure(bg='#efe5d9')

        # create Stay Frame
        stay_frame = LabelFrame(self)
        stay_frame.grid(row=0, column=0)

        # define universal styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', font=('Nexa', '10'), background='white'    )
        self.option_add('*TCombobox*Listbox.font', ('Nexa', '10')               )
        style.configure('TEntry', font='Arial 10'                               )
        style.configure('TRadiobutton', font='Arial 10', background='#f9f5f0'   )
        style.configure('TCheckbutton', font='Nexa 10', background='#f9f5f0'    )
        style.configure('TButton', font='San_Francisco 9', background='white'   )



class Home(ttk.Frame):


    button_settings = { 'width': 20,
                        'font': 'Lato 13 bold',
                        'bg': 'white',
                        }

    button_options = {
                        }


    def __init__(self, container):

        super().__init__(container)
        self.container = container

        # Create MAIN MENU Frame #
        self.main_menu =    LabelFrame( self.container,
                                        padx=40,
                                        pady=40
                                        )
        self.main_menu.grid(            row=0,
                                        column=0,
                                        padx=20,
                                        pady=20
                                        )

        # MAIN MENU BUTTONS #
        new_stay_button =   Button(     self.main_menu,
                                        text='New Stay',
                                        command=self.start_new_stay,
                                        **self.button_settings
                                        )
        pull_stay_button =  Button(     self.main_menu,
                                        text='Search Stays',
                                        command=self.pull_a_stay,
                                        **self.button_settings
                                        )
        pull_clean_button = Button (    self.main_menu,
                                        text='Clean Details',
                                        command=self.clean_a_stay,
                                        **self.button_settings)

        # place menu buttons in main_menu frame

        row_count = 0
        for button in (new_stay_button, pull_stay_button, pull_clean_button):

            button.grid(row=row_count, column=0, padx=10, pady=10)

            row_count += 1


        self.stay_on = False
        self.pull_on = False
        self.clean_on = False



    def start_new_stay(self):

        self.reset_frame()

        self.stay_on = True

        # initialise all three starting frames by instantiating the MainFrames class
        self.new_stay = Stay(self.container, 'new')



    def pull_a_stay(self):

        self.reset_frame()

        self.pull_on = True

        self.pull_stay = Pull(self.container, 'stay')



    def clean_a_stay(self):

        self.reset_frame()

        self.clean_on = True

        self.pull_clean = Pull(self.container, 'clean')



    def reset_frame(self):

        try:
            if self.pull_stay.stay_pulled == True:
                self.pull_stay.throw.destroy_frames()
                self.pull_on = False
                self.pull_stay.stay_pulled = False

            elif self.stay_on == True:

                self.new_stay.destroy_frames()
                self.stay_on = False

            elif self.pull_on == True:

                self.pull_stay.destroy_frames()
                self.pull_on = False

            elif self.clean_on == True:

                self.pull_clean.destroy_frames()
                self.clean_on = False

            else: pass

        except:
            if self.stay_on == True:

                self.new_stay.destroy_frames()
                self.stay_on = False

            elif self.pull_on == True:

                self.pull_stay.destroy_frames()
                self.pull_on = False

            elif self.clean_on == True:

                self.pull_clean.destroy_frames()
                self.clean_on = False

            else: pass



if __name__ == '__main__':
    app = App()
    Home(app)
    app.mainloop()
