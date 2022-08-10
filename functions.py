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


def main():
    pass

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
    prc = ('65.00', '75.00', '85.00', '95.00', '105.00', '115.00')

    if bed_number == 1 and people <= 2:
        return cln[0], prc[0]
    elif bed_number == 1:
        return cln[1], prc[1]

    elif bed_number == 2 and people <= 4:
        return cln[0], prc[2]
    elif bed_number == 2:
        return cln[1], prc[3]

    elif bed_number == 3 and people <= 6:
        return cln[0], prc[4]
    else:
        return cln[1], prc[5]


# simple function to split a date string formatted as 'dd/mm/yyyy'
def split_date(date):

    split = date.split('/')

    day =   int(split[0])
    month = int(split[1])
    year =  int(split[2])

    return day, month, year


# function to calculate the number of days difference between two given dates
def count_days(in_date, out_date):

    # break up arrival and departure dates according to their 'dd/mm/yyyy' format
    # call on split_dates() function
    in_day, in_month, in_year =     split_date(in_date)
    out_day, out_month, out_year =  split_date(out_date)

    # first, establish difference between months to accurately count days left
    # in first month to subtract from in_day if stay spills into another month
    if in_month == out_month and in_year == out_year:
        first_month = 0
    else:
        first_month = days_in_month(in_month, in_year)

    # conditionals to determine the right mathematical considerations to apply
    if in_year == out_year:
        # check nº of months apart
        in_between_days = days_in_months(in_month, out_month, in_year)
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
        # check for nº of days left in months apart from in and out months
        old_year_months_by_days = days_in_months(
                                                    in_month,
                                                    12,
                                                    in_year,
                                                    old_year=True
                                                )
        new_year_months_by_days = days_in_months(
                                                    1,
                                                    out_month,
                                                    out_year,
                                                    new_year=True
                                                )
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

    for m in thirty1:   # check for a 31-day month  ## most likely ##
        if month == m:
            return 31

    for m in thirty:    # check for a 30-day month
        if month == m:
            return 30

    if month == 2:   # check for a February month
        if year not in (2020, 2024, 2028, 2032):   # check for leap
            return 28
        else:
            return 29


# calculates the number of days between two months at least two months apart
# if not two months apart, returns 0
def days_in_months(start_month, end_month, year, old_year=False, new_year=False):

    if end_month - start_month == 0:
        return 0

    else:
        # prepare tuples of months and months by nº of days
        months = (1, 2, 3, 5, 5, 6, 7, 8, 9, 10, 11, 12)
        days_in_between = 0

        if old_year == True:
            rng = range(start_month, 12) # index from 1 above start until Dec
        elif new_year == True:
            rng = range(0, end_month - 1) # index from Jan until 1 below end
        else:
            rng = range(start_month, end_month - 1) # index between start and end months

        for n in rng:
            days_in_between += days_in_month(months[n], year)

        return days_in_between


# function to set pre-generated arrival and departure dates in the Main Frame
# date entry tkcalendar function. Takes args: date string in 'dd/mm/yyyy' format
# and specification for type of date, arrival or departure. Will add 14 days to
# arrival date and 21 to departure date
def set_date(date, added):

    # convert dd, mm, and yyyy to integer for simple processing
    day, month, year = split_date(date)

    # check for which direction of travel for new date setting
    if added > 0:
        change = 1
    else:
        change = -1
        added = -(added) # change negative given to positive for iteration

    for _ in range(added):
        day += change

        month_days = days_in_month(month, year) # call once to prep for next

        if day > month_days:
            day = 1
            month += 1
            if month == 13:
                month = 1
                year += 1

        if day == 0:
            day = month_days
            month -= 1
            if month == 0:
                month = 12
                year -= 1

    return date_string(day, month, year)


def date_string(day, month, year):

    date = ''

    if day < 10:    # look for need to add '0' to the day of final string
        date += '0'
    date += str(day) + '/'      # add forward-slash separator
    if month < 10:  # look for need to add '0' to the month of final string
        date += '0'
    date += str(month) + '/' + str(year) # finish with last separator and year

    return date


# returns a list of strings of all dates between two given dates, inclusive
def between_dates(start, end):

    counted_days = count_days(start, end)

    dates_list = list()

    present_date = start

    for _ in range(counted_days):
        next_date = set_date(present_date, 1)
        present_date = next_date
        dates_list.append(next_date)


    return dates_list


if __name__ == '__main__':
    main()
