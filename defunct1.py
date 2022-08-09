# universal function for cancel button option #
# destroys window and returns [0]
def cancel(window):
    window.destroy()
    return [0]

# universal function for save button option #
# destroys window and returns a list with necessary values
def save(*args):
    # set result[0] at integer 1 for posterior iteration in main code
    result = [1]
    for arg in args[1:]:
        result.append(arg)
    args[0].destroy()
    return result

# function to provide custom charge description in a pop-up window #
def custom_charge_description():

    custom_window = Toplevel(bg='#fbf9f6')
    custom_window.title('Add details for charge')
    description_label = ttk.Label(chargec_window, text='Description',
                        background='#fbf9f6')
    description_label.grid(row=0, column=0, padx=20, pady=10, sticky=W)
    description_box = Text(custom_window, width=17, height=1,
                                font='Arial 11')
    description_box.grid(row=1, column=0, padx=20, sticky=W)

    # generate save and cancel options
    save_button = ttk.Button(custom_window, text='Save', width=5
        command=lambda: save(custom_window, description_box.get(1.0, 'end-1c')))
    save_button.grid(row=3, column=1, padx=10, pady=10)

    cancel_button = ttk.Button(custom_window, text='Cancel', width=7,
        command=lambda: cancel(custom_window))
    cancel_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)
