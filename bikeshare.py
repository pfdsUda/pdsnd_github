import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_ARRAY = [ 'all', 'january', 'february', 
                'march', 'april', 'may', 'june' ]

DAYS_ARRAY = [ 'all', 'monday', 'tuesday', 'wednesday', 
              'thursday', 'friday', 'saturday', 'sunday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWhich city would you like to explore? Enter [Chicago, New York City or Washington]\n')
        if (city.lower() == 'chicago') | (city.lower() == 'new york city') | (city.lower() == 'washington'):
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month would you like to explore? Enter [All, January, February, March, April, May or June]\n')
        found = False
        for(m) in MONTH_ARRAY:
            if m.lower() == month.lower():
                found = True
                break
        if found:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhich day would you like to explore? Enter [All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday]\n')
        found = False
        for(d) in DAYS_ARRAY:
            if d.lower() == day.lower():
                found = True
                break
        if found:
            break

    print('-'*40)
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
    
    city_file = city.lower().replace(" ","_") + ".csv"
    df = pd.read_csv(city_file)
    
    month = MONTH_ARRAY.index(month.lower())
    day = DAYS_ARRAY.index(day.lower())
    
    if month != 0:
        month_filter = (pd.to_datetime(df['Start Time']).dt.month == month)
        df = df[month_filter]
            
    if day != 0:
        day_filter = (pd.to_datetime(df['Start Time']).dt.dayofweek == (day-1))
        df = df[day_filter]
        
    print("File loaded:\t%s" % city_file)
    print("Selected month:\t%s" % MONTH_ARRAY[month].title())
    print("Selected day:\t%s" % DAYS_ARRAY[day].title())
    print('-'*40)
            
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    mc_month = pd.to_datetime(df['Start Time']).dt.month.mode()[0]
    print("Most common month is:\t%s" % MONTH_ARRAY[mc_month].title())

    # display the most common day of week
    mc_day = pd.to_datetime(df['Start Time']).dt.day_name().mode()[0]
    print("Most common day of week is:\t%s" % mc_day)
    
    # display the most common start hour
    mc_hour = pd.to_datetime(df['Start Time']).dt.hour.mode()[0]
    print("Most common start hour is:\t%2d:00" % mc_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start = df['Start Station'].mode()[0]
    print("Most common start station is:\t\t%s" % mc_start)
    
    # display most commonly used end station
    mc_end = df['End Station'].mode()[0]
    print("Most common end station is:\t\t%s" % mc_end)

    # display most frequent combination of start station and end station trip
    df_combine = df['Start Station'].str.cat(df['End Station'], sep = ' -> ')
    stations = df_combine.mode()[0]
    print("Most common start and end station is:\t%s" % stations)       
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time is:\t%.2d minutes (%.1f hours)" % (total_time,total_time/60.0))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("Total average time is:\t%.1f minutes (%.1f hours)" % (avg_time,avg_time/60.0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("\nCounts of user types are:")
    print('-'*25)
    print(user_type.to_string())

    # Display counts of gender (check of column exists)
    if 'Gender' in df:
        genders = df['Gender'].value_counts()
        print("\nCounts of gender types are:")
        print('-'*27)
        print(genders.to_string())

    # Display earliest, most recent, and most common year of birth (check of column exists)
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
    
        print("\nEarliest year of birth:\t%d" % earliest)
        print("Most recent year of birth:\t%d" % recent)
        print("Most common year of birth:\t%d" % common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data."""
    i = 0
    raw = input("\nWould you like to see raw data? Type 'yes' or 'no'\n")
    pd.set_option('display.max_columns',200)
    
    total_rows = df.shape[0]

#Wait until user stops by saying no
    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            if i > total_rows:
                print("\nNo more data.\n")
                raw = 'no'
            else:
                print(df.iloc[i:(i-1)+5,:])
                print("\nShowing rows %d-%d of %d..." % (i,(i-1)+5,total_rows))
                raw = input("\nWould you like to see more raw data? Type 'yes' or 'no'\n")
                i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
"""Added a new comment for the refactoring branch."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
	main()
