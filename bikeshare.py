# Explore US Bikeshare data

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')


    # get user input for city
    city = input('Which city would you like to see? Please type Chicago, Washington or New York City.\n ' ).lower()
    while city not in CITY_DATA.keys():
        city = input('Oops! An error ocurred. Please choose either Chicago, Washington or New York City and check your input for typos.\n ').lower()


    # get user input for month (all, january, february, ... , june)
    month = input('Please select a month. You can also type "all" to see statistics for all monthes in the data set.\n ').lower()[0:3]
    while month not in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'all']:
        month = input('Oops! An error ocurred. Please choose a month from january to june or "all" if you do not want to filter by month and check your input for typos.\n ').lower()[0:3]


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('What day are you interested in? Type mon, tue, wed, thu, fri, sat or sun for a specific day or "all" if you do not want to filter by day.\n ').lower()[0:3]
    while day not in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']:
        day = input('Oops! An error ocurred. Please choose a day of the week or "all" if you do not want to filter by day and check your input for typos.\n ').lower()[0:3]

    print('-'*40)
    print('Great! You made the following choices: \n City: {} \n Month: {} \n Day: {}'. format(city.capitalize(), month, day))
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    months_map = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun', 7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'}
    df['month'] = df['month'].apply(lambda monthint: months_map[monthint])

    df['day'] = df['Start Time'].dt.weekday_name
    df['day'] = df['day'].apply(lambda daylong: daylong.lower()[0:3])


    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day]

    return df

def display_data(df):
    """
    Gives user the option to display the filtered raw data.
    Displays 5 rows at a time unless user chooses to proceed.
    """

    raw_data_choice = input('\nWould you like to take a look at the raw data?\nType yes to see the first rows of your selected data set or no to proceed to explore some summarizing statistics.\n ').lower()
    i = 1
    while raw_data_choice == 'yes':
        lowerind = ((i-1) * 5)
        upperind = (i * 5)
        print('Displaying rows ', lowerind, ' to ', upperind - 1, '.')
        print(df[lowerind : upperind])
        i = i + 1
        raw_data_choice = input('Would you like to see the next five rows of raw data? Enter yes or no.\n ').lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is', most_common_month)

    # display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('The most common day of the week is', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common start hour is', most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('The most common Start Station is', most_common_start)

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('The most common End Station is', most_common_end)

    # display most frequent combination of start station and end station trip
    df['Start End combination'] = df['Start Station'] + ' and ' + df['End Station']
    most_common_combi = df['Start End combination'].mode()[0]
    print('The most common Start End combination is', most_common_combi)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_min, total_s = divmod(total_travel_time, 60)
    total_h, total_m = divmod(total_min, 60)
    print('Total travel time was {} hours, {} minutes and {} seconds.'.format(int(total_h), int(total_m), int(total_s)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_min, mean_s = divmod(mean_travel_time, 60)
    mean_h, mean_m = divmod(mean_min, 60)
    print('Average travel time was {} hours, {} minutes and {} seconds.'.format(int(mean_h), int(mean_m), int(mean_s)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('Counts of user types:\n', user_counts, '\n')

    # Display counts of gender
    if city != 'washington':
        gender_counts = df['Gender'].value_counts()
        print('Counts of user gender:\n', gender_counts, '\n')
    else:
        print('Gender counts: The variable gender is not contained in the selected data set.')

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode())
        print('The oldest user was born in {}.\nThe youngest user was born in {}.\nThe most common birth year of users was {}.\n'.format(earliest_birth, most_recent_birth, common_birth))
    else:
        print('User age: Error. The variable birth year is not contained in the selected data set.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
