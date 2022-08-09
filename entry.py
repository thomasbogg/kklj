from tkinter import *
from tkcalendar import Calendar, DateEntry

root = Tk()


Entry(root).pack()

date = StringVar()
DateEntry(root, slectmode='day', textvariable=date,
                    locale='en_UK',
                    width=14).pack()

print(date.get())

root.mainloop()
