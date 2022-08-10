from functions import *

def main():

    test_split_date()
    test_count_days()
    test_days_in_month()
    test_set_date()


def test_split_date():
    assert split_date('12/09/2003') == (12, 9, 2003)
    assert split_date('01/01/1000') == (1, 1, 1000)
    assert split_date('10/08/2022') == (10, 8, 2022)

def test_count_days():
    assert count_days('01/01/2021', '01/01/2022') == 366
    assert count_days('01/01/2022', '10/01/2022') == 9
    assert count_days('10/10/2020', '31/12/2020') == 82
    assert count_days('10/02/2020', '10/02/2021') == 367

def test_days_in_month():
    assert days_in_month(1, 2002) == 31
    assert days_in_month(2, 2024) == 29
    assert days_in_month(2, 2022) == 28
    assert days_in_month(9, 2023) == 30

def test_set_date():
    assert set_date('01/01/2003', 10) == '11/01/2003'
    assert set_date('10/08/2022', 21) == '31/08/2022'
    assert set_date('10/08/2022', 51) == '30/09/2022'
    assert set_date('10/08/2022', -11) == '30/07/2022'
    assert set_date('10/08/2022', -365) == '10/08/2021'

if __name__ == '__main__':
    main()
