import time
import pandas as pd
import numpy as np
import csv

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

DAYS_IN_VALS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

MONTHS_IN_VALS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington?\n').strip().lower()
    while city not in CITY_DATA.keys():
        city = input('Wrong input, please enter the right city \
(Chicago, New York City, or Washington): \n').strip().lower()

    filtering_key = input('Would you like to filter the data by month, day, both, or not at all? \
Type (none) for no time filter.\n').strip().lower()

    while filtering_key not in {'month', 'day', 'none', 'both'}:
        filtering_key = input('wrong input! Would you like to filter the data by month, day, both, or not at all? \
Type (none) for no time filter.\n').strip().lower()

    if filtering_key == 'month':
        month = get_month()
        day = 'all'

    elif filtering_key == 'day':
        month = 'all'
        day = get_day()

    elif filtering_key == 'both':
        month = get_month()
        day = get_day()

    elif filtering_key == 'none':
        month = 'all'
        day = 'all'

    print('-' * 40)
    return city, month, day


def get_month():
    """ get user input for month (all, january, february, ... , june)"""

    month = input('(If they chose month) Which month \
- January, February, March, April, May, or June?\n').strip().lower()
    months = set(MONTHS_IN_VALS)
    while month not in months:
        month = input('Wrong input, \
please try to enter the month name again - January, \
February, March, April, May, or June?\n').strip().lower()

    return month


def get_day():
    """ get user input for day of week (all, monday, tuesday, ... sunday)"""

    day = input('(If they chose day) Which day - \
Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').strip().lower()
    days = set(DAYS_IN_VALS)
    while day not in days:
        day = input('Wrong input, please try to enter the day name again - \
Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').strip().lower()
    return day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('What is the most popular month for travelling?\n', MONTHS_IN_VALS[df['month'].mode()[0] - 1].title())

    # display the most common day of week
    print('what is the most popular day of week for travelling?\n', df['day_of_week'].mode()[0].title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('what is the most popular hour of the day to start travelling?\n', df['hour'].mode()[0])

    execution_time =(time.time() - start_time)
    print(f"\nThis took {execution_time} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    m_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', m_start_station)

    # display most commonly used end station
    m_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: ', m_end_station)

    # display most frequent combination of start station and end station trip
    df['start_to_end_station'] = df['Start Station'] + " To " + df['End Station']
    m_start_to_end_station = df['start_to_end_station'].mode()[0]
    print('The most frequent combination of start station and end station trip:\nFrom ', m_start_to_end_station)

    execution_time =(time.time() - start_time)
    print(f"\nThis took {execution_time} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # two solutions one with numpy(more efficient) and the second by pandas methods.
    total_travel_time = np.sum(df['Trip Duration'])  # total_travel_time = df['Trip Duration'].sum()
    print('The total travel time: ', convert_seconds(int(total_travel_time)))

    # display mean travel time
    # two solutions one with numpy(more efficient) and the second by pandas methods
    mean_travel_time = np.mean(df['Trip Duration'])  # mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time: ', convert_seconds(int(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("What is the breakdown of users?\n", user_types)
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('What is the breakdown of gender?\n', gender_count)
        print()
    else:
        print('No gender data to show!')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_y_o_b = int(df['Birth Year'].min())
        most_recent_y_o_b = int(df['Birth Year'].max())
        most_common_y_o_b = int(df['Birth Year'].mode()[0])

        print('Year of birth breakdown:\nearliest: {}\n most recent: \
{}\nmost common: {}'.format(earliest_y_o_b, most_recent_y_o_b, most_common_y_o_b))
    else:
        print('No Birth Year data to show!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def read_csv_in_rows(filename):
    """
    Reads a CSV file and processes it row by row.

    Args:
        filename (str): The name of the CSV file to be read.

    Returns:
         None

    Description:
        This function reads a CSV file and processes it row by row using the csv.DictReader.
        It accumulates the rows in a list of 5 and calls the 'print_rows' function to handle the list.
        After processing each batch, it prompts the user to decide whether to view new individual trip data or not.
        If the user chooses 'no', the function breaks out of the loop and stops processing the file.

    Example:
        read_csv_in_rows('data.csv')
    """

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        rows = []

        for row in reader:
            rows.append(row)
            if len(rows) == 5:
                print_rows(rows)
                rows = []

                continue_printing = input('\nWould you like to view individual trip data?\
Type \'yes\' or \'no\'.\n').strip().lower()

                while continue_printing not in ['yes', 'no']:
                    continue_printing = input('\nwrong input!!, Would you like to view individual\
trip data? Type \'yes\' or \'no\'.\n').strip().lower()

                if continue_printing == 'no':
                    break

        if rows:
            print_rows(rows)
            print('\nThe end of row data!')


def print_rows(rows):
    """
    Prints the rows of data.

    Args:
        rows (list): A list of rows(dictionary rows) to be printed.

    Returns:
         None

    Description:
        This function takes a list of rows as input and prints each row.
        It iterates over the provided rows and prints each row using the 'print' function.

    """

    for row in rows:
        print(row)


def get_most_common_season(city):
    """
    Determines the most popular season for traveling in a specified city.

    Args:
        city (str): The name of the city for which to determine the most popular season.

    Returns:
        str: The most common season for traveling in the specified city.
    """

    start_time = time.time()
    df = load_data(city, 'all', 'all')
    most_common_month = df['month'].mode()[0]

    if most_common_month in [12, 1, 2]:
        most_common_season = 'Winter'
    elif most_common_month in [3, 4, 5]:
        most_common_season = 'Spring'
    elif most_common_month in [6, 7, 8]:
        most_common_season = 'Summer'
    else:
        most_common_season = 'Fall'

    # Displaying the most common season
    print('What is the most popular season for travelling in {}?\nThe most common season is {}.'
          .format(city, most_common_season))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def convert_seconds(seconds):
    """
    Converts a number of seconds into the format of (n days, s hours, x minutes, y seconds).

    Args:
        seconds (int): The total number of seconds to be converted.

    Returns:
        str: The formatted string representing the converted time.
    """

    days = seconds // (24 * 60 * 60)
    remaining_seconds = seconds % (24 * 60 * 60)
    hours = remaining_seconds // (60 * 60)
    remaining_seconds = remaining_seconds % (60 * 60)
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    result = "{} days, {} hours, {} minutes, {} seconds.".format(days, hours, minutes, seconds)
    return result


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Some information from the data
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_most_common_season(city)

        # Ask the user if he wants to see the 5 lines row data or not.
        show_row_data = input('Do you want to see 5 lines of raw data? Enter "yes" or "no".\n').strip().lower()
        while show_row_data not in ['yes', 'no']:
            show_row_data = input('\nWrong input!!, Do you want to see 5 lines of raw data?\
 Enter "yes" or "no".\n').strip().lower()

        if show_row_data == 'yes':
            print('Printing 5 lines of row data:\n')
            read_csv_in_rows(CITY_DATA[city])

        # Ask the user if he wants to restart the program again or not.
        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        while restart not in ['yes', 'no']:
            restart = input('\nWrong input!!, Would you like to restart? Enter yes or no.\n').strip().lower()

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
