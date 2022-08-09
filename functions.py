"""
    MODULE OF SUPPLEMENTARY FUNCTIONS to support process of calculations
    for Charges Function in Stay Class of KKLJ Property Management App.
    Here, functions include:

            -   determining clean charge for given property and nº of people;
            -   determining the length of stay of a given period,
                    with month length determination supplementary function;
            -
"""


# import sqlite3 to access database for property info
# Properties table in DB is composed: id, name, bedrooms, owner, email
import sqlite3



# function to return accurate description and charge of the clean
def clean_calc(property, people):

    # use the DB to locate property row and number of bedrooms
    conn = sqlite3.connect('KKLJ.db')
    cur = conn.cursor()

    cur.execute('SELECT bedrooms FROM Properties WHERE name=?', (property,))
    bed_no = cur.fetchone()[0]  # variable to hold correct num of bedrooms
    # cleaning prices are dependent on nº of bedrooms and nº of people staying

    if bed_no == 1:
        if people <= 2:
            return 'Full Clean', '65.00'
        else:
            return 'Full Clean +pax', '75.00'
    elif bed_no == 2:
        if people <= 4:
            return 'Full Clean', '85.00'
        else:
            return 'Full Clean +pax', '95.00'
    else:
        if people <= 6:
            return 'Full Clean', '105.00'
        else:
            return 'Full Clean +pax', '115.00'



# function to calculate the number of days difference between two given dates
def count_days(in_date, out_date):

    # break up arrival and departure dates according to their 'dd/mm/yyyy' format
    # dates are given as strings
    # GLOSSARY:
        # - arr : arrival
        # - der : departure
    arr_day =   int(in_date[0:2])
    arr_month = int(in_date[3:5])
    arr_year =  int(in_date[6:])

    der_day =   int(out_date[0:2])
    der_month = int(out_date[3:5])
    der_year =  int(out_date[6:])

    # prepare tuples of months and months by nº of days
    months = (  1, 2, 3, 5, 5, 6,
                7, 8, 9, 10, 11, 12 )

    # conditionals to determine the right mathematical considerations to apply
    if arr_year == der_year:

        if arr_month == der_month:  # if months same, simple subtraction
            return der_day - arr_day

        else:
            # establish number of days in arrival month, call on suppl function
            first_month = days_in_month(arr_month, arr_year)
            # check nº of months apart
            difference = der_month - arr_month
            if difference == 1:     # if only 1 month diff, ## most likely ##
                return first_month - arr_day + der_day

            else:
                # get index values of months for new iteration
                months_by_days = 0  # initiate variable to hold number of days per month
                # looking for months after arr_month and before der_month
                for n in range(     months.index(arr_month) + 1,
                                    months.index(der_month)         ):

                    months_by_days += days_in_month(months[n], arr_year)

                # return with numbers of days of months in between
                return (    first_month -
                            arr_day +
                            der_day +
                            months_by_days  )
    else:
        # safely presume the difference between years is never more than 1
        # focus on determining months between
        first_month = days_in_month(arr_month, arr_year)
        # check for nº of months left in arr_year
        months_left_arr_year = 12 - arr_month
        # start arr year months days count at 0, add if months in between
        old_year_months_by_days = 0
        if months_left_arr_year > 0:
            # iterate to determine days left in months arr year
            # start at 1 (because > 0) and stop at one number before months left
            for n in range(1, months_left_arr_year + 1):
                old_year_months_by_days += days_in_month(months[arr_month -
                                                                1 + n],
                                                                arr_year        )

        # now do the same for months until departure
        # simple index of month in months will give correct number
        months_left_der_year = months.index(der_month)
        # start der year months days count a 0, add if months in between
        new_year_months_by_days = 0
        if months_left_der_year > 0:
            for n in range(0, der_month - 1):
                new_year_months_by_days += days_in_month(months[n], der_year)

        return (    first_month - arr_day +
                    old_year_months_by_days +
                    new_year_months_by_days +
                    der_day                     )



# suppl of the days_in_stay function, to determine nº of days in given month
def days_in_month(month, year):
    thirty = (  4, 6, 9, 11             )
    thirty1 = ( 1, 3, 5, 7, 8, 10, 12   )
    for m in thirty:    # check for a 30-day month
        if month == m:
            return 30
    for m in thirty1:   # check for a 31-day month
        if month == m:
            return 31
    if month == 2:   # check for a February month
        if year != 2024 and year != 2028:   # check for leap
            return 28
        else:
            return 29



# function to set pre-generated arrival and departure dates in the Main Frame
# date entry tkcalendar function. Takes args: date string in 'dd/mm/yyyy' format
# and specification for type of date, arrival or departure. Will add 14 days to
# arrival date and 21 to departure date
def set_date(date, type):

    # convert dd, mm, and yyyy to integer for simple processing
    day =   int(date[:2])
    month = int(date[3:5])
    year =  int(date[6:])


    # check type of date being processed, add relevant future time respectively
    if type == 'e':       # 'e' for end_date
        added = 7
    elif type == 'a':     # 'a' for arrival
        added = 14
    elif type == 'd':     # 'd' for departure
        added = 21
    elif type == '-5':    # '-5' for the last 5 days
        added = -5

    # call on days_in_month() in this module to determine month length
    month_length = days_in_month(month, year)

    # conditional to check what adjustments need to be made to the dates
    if day + added > month_length:
        fut_day = day + added - month_length
        # check for December-January, just add 1 to month if not
        if month == 12:
            fut_month = 1
            fut_year = year + 1
        else:
            fut_month = month + 1
            fut_year = year
    elif day + added <= 0:
        if month == 1:
            fut_month = 12
            fut_year = year - 1
        else:
            fut_month = month - 1
            fut_year = year
        fut_day = days_in_month(fut_month, fut_year) + day + added
    else:
        fut_day = day + added
        fut_month = month
        fut_year = year


    # prepare string for return
    fut_date = ''
    if fut_day < 10:    # look for need to add '0' to the day of final string
        fut_date += '0' + str(fut_day)
    else:
        fut_date += str(fut_day)
    fut_date += '/'     # add forward-slash separator
    if fut_month < 10:  # look for need to add '0' to the month of final string
        fut_date += '0' + str(fut_month)
    else:
        fut_date += str(fut_month)
    fut_date += '/' + str(fut_year) # finish with last separator and year


    return fut_date


# returns a list of strings of all dates between two given dates, inclusive
def between_dates(start, end):

    start_d = int(start[:2])
    start_m = int(start[3:5])
    start_y = int(start[6:])

    end_d = int(end[:2])
    end_m = int(end[3:5])
    end_y = int(end[6:])

    dates_list = list()

    if start_y == end_y:

        if start_m == end_m:

            for day in range(start_d, end_d + 1):

                if len(str(day)) == 1:
                    day_string = '0' + str(day)
                else:
                    day_string = str(day)

                date_string = day_string + start[2:]

                dates_list.append(date_string)

        else:
            # look for the rest of the days of start month
            for day in range(start_d, days_in_month(start_m, start_y) + 1):

                if len(str(day)) == 1:
                    day_string = '0' + str(day)
                else:
                    day_string = str(day)

                date_string = day_string + start[2:]

                dates_list.append(date_string)


            # look for in-between months
            if end_m - start_m > 1:

                for month in range(start_m + 1, end_m):

                    if len(str(month)) == 1:
                        month_string = '0' + str(month)
                    else:
                        month_string = str(month)

                    for day in range(1, days_in_month(month, start_y) + 1):

                        if len(str(day)) == 1:
                            day_string = '0' + str(day)
                        else:
                            day_string = str(day)

                        date_string = day_string + '/' + month_string + start[5:]

                        dates_list.append(date_string)


            # add the leftover end month days
            for day in range(1, end_d + 1):

                if len(str(day)) == 1:
                    day_string = '0' + str(day)
                else:
                    day_string = str(day)

                date_string = day_string + end[2:]

                dates_list.append(date_string)


    else:

        # look for the rest of the days of start month
        for day in range(start_d, days_in_month(start_m, start_y) + 1):

            if len(str(day)) == 1:
                day_string = '0' + str(day)
            else:
                day_string = str(day)

            date_string = day_string + start[2:]

            dates_list.append(date_string)


        if start_m < 12:
            # look for the days in the rest of the months of the start year
            for month in range(start_m, 13):

                if len(str(month)) == 1:
                    month_string = '0' + str(month)
                else:
                    month_string = str(month)

                for day in range(1, days_in_month(month, start_y) + 1):

                    if len(str(day)) == 1:
                        day_string = '0' + str(day)
                    else:
                        day_string = str(day)

                    date_string = day_string + '/' + month_string + start[5:]

                    dates_list.append(date_string)

        if end_m > 1:
            for month in range(1, end_m):

                if len(str(month)) == 1:
                    month_string = '0' + str(month)
                else:
                    month_string = str(month)

                for day in range(1, days_in_month(month, end_y) + 1):

                    if len(str(day)) == 1:
                        day_string = '0' + str(day)
                    else:
                        day_string = str(day)

                    date_string = day_string + '/' + month_string + end[5:]

                    dates_list.append(date_string)


        # add the leftover end month days
        for day in range(1, end_d + 1):

            if len(str(day)) == 1:
                day_string = '0' + str(day)
            else:
                day_string = str(day)

            date_string = day_string + end[2:]

            dates_list.append(date_string)


    return dates_list
