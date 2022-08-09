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
    bed_number = cur.fetchone()[0]  # variable to hold correct num of bedrooms
    # cleaning prices are dependent on nº of bedrooms and nº of people staying

    # two options for the clean: Normal Full or Extra Person Full
    cln = ('Full Clean', 'Full Cln +pax')

    if bed_number == 1:
        if people <= 2:
            return cln[0], '65.00'
        else:
            return cln[1], '75.00'
    elif bed_number == 2:
        if people <= 4:
            return cln[0], '85.00'
        else:
            return cln[1], '95.00'
    else:
        if people <= 6:
            return cln[0], '105.00'
        else:
            return cln[1], '115.00'


# simple function to split a date string formatted as 'dd/mm/yyyy'
def split_date(date):

    split = date.split('/')

    day =   split[0]
    month = split[1]
    year =  split[2]

    return day, month, year


# function to calculate the number of days difference between two given dates
def count_days(in_date, out_date):

    # break up arrival and departure dates according to their 'dd/mm/yyyy' format
    # call on split_dates() function
    in_day, in_month, in_year =     split_date(in_date)
    out_day, out_month, out_year =  split_date(out_date)


    # conditionals to determine the right mathematical considerations to apply
    if in_year == out_year:

        if in_month == out_month:  # if months same, simple subtraction
            first_month = 0
        else:
            # establish number of days in arrival month, call on suppl function
            first_month = days_in_month(in_month, in_year)

        # check nº of months apart
        in_between_days = days_by_months(in_month, out_month, in_year)

        # return with numbers of days of months in between, could be 0
        return (
                        first_month     -
                        in_day          +
                        out_day         +
                        in_between_days
                    )
    else:
        # safely presume the difference between years is never more than 1
        # focus on determining months between
        first_month = days_in_month(in_month, in_year)
        # check for nº of days left in months apart from in and out months
        old_year_months_by_days = days_in_months(in_month, 12, in_year)
        new_year_months_by_days = days_in_months(1, out_month, out_year)

        return (
                    first_month             -
                    in_day                  +
                    old_year_months_by_days +
                    new_year_months_by_days +
                    out_day
                )


# suppl of the days_in_stay function, to determine nº of days in given month
def days_in_month(month, year):

    thirty1 = ( 1, 3, 5, 7, 8, 10, 12   )
    thirty = (  4, 6, 9, 11             )

    for m in thirty1:   # check for a 31-day month
        if month == m:
            return 31

    for m in thirty:    # check for a 30-day month
        if month == m:
            return 30

    if month == 2:   # check for a February month
        if year != 2024 and year != 2028:   # check for leap
            return 28
        else:
            return 29


# calculates the number of days between two months at least two months apart
def days_in_months(start_month, end_month, year):

    if end_month - start_month == 0:
        return 0

    else:
        # prepare tuples of months and months by nº of days
        months = (1, 2, 3, 5, 5, 6, 7, 8, 9, 10, 11, 12)
        days_in_between = 0

        for n in range(months.index(start_month) + 1, months.index(end_month)):

            days_in_between += days_in_month(months[n], year)

        return days_in_between


# function to set pre-generated arrival and departure dates in the Main Frame
# date entry tkcalendar function. Takes args: date string in 'dd/mm/yyyy' format
# and specification for type of date, arrival or departure. Will add 14 days to
# arrival date and 21 to departure date
def set_date(date, type):

    # convert dd, mm, and yyyy to integer for simple processing
    day, month, year = split_dates(date)

    # check type of date being processed, add relevant future time respectively
    if type == 'e':       # 'e' for end_date
        added = 7
    elif type == 'a':     # 'a' for arrival in 14 days
        added = 14
    elif type == 'd':     # 'd' for departure in 21 days
        added = 21
    elif type == '-5':    # '-5' for 5 days ago
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

    # split dates into their components, call on function
    s_day, s_month, s_year =    split_date(start)
    e_day, e_month, e_year =    split_date(end)

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
