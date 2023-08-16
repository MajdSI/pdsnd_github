import time
import pandas as pd
import numpy as np


CITY_DATA = {
    'chicago': 'chicago.csv',
    'newyorkcity': 'new_york_city.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def check_data_entry(prompt, valid_entries): 
    """
    Function that asks the user to input data and verifies if it's valid.
    This simplifies the get_filters() function, where we need to ask the user for three inputs.
    Args:
        (str) prompt - message to show to the user
        (list) valid_entries - list of accepted strings 
    Returns:
        (str) user_input - user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()
        while user_input not in valid_entries : 
            print('It looks like your entry is incorrect.')
            print("Let's try again!")
            user_input = str(input(prompt)).lower()

        print("Great! You've chosen: {}\n".format(user_input))
        return user_input

    except:
        print('There seems to be an issue with your input.')

def get_filters(): 
    """
    Function to ask the user for a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day

#-----------------------------------------------------------------------------------

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
    
    file_path = CITY_DATA[city]

    df = pd.read_csv(file_path)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['jan','feb','mar','apr','may','jun']  # Use first three letters of month name
        month = months.index(month[:3]) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



#-----------------------------------------------------------------------------------

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print(f"The most common month: {common_month}")

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    print(f"The most common day: {common_day}")

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    most_common_hour = df["hour"].mode()[0]
    print(f"The most common hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
#-----------------------------------------------------------------------------------

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print(f'The most common start station used: {common_start_station}')

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print(f'The most common end station used: {common_end_station}')

    # display most frequent combination of start station and end station trip
    frequent_start_end_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(f'The most frequent combination of start station and end station trip:\n {frequent_start_end_station}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

 #-----------------------------------------------------------------------------------

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600.0
    print(f'The total travel time: {total_travel_time}')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600.0
    print(f'The mean travel time: {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

  #----------------------------------------------------------------------------------

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'The number of user types: {user_types}')

    # Display counts and percentage of gender
    if 'Gender' not in df.columns:
        print("The city's data don't have gender :(")
    else:
        user_gender = df['Gender'].value_counts()
        total_users = len(df)
        gender_percentage = (user_gender / total_users) * 100
        print(f'The number of gender:\n{user_gender}')
        print(f'Gender percentage distribution:\n{gender_percentage}')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print("The city's data don't have birth year :(")
    else:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].value_counts().idxmax())

        print(f'The earliest year of birth: {earliest}')
        print(f'The most recent year of birth: {most_recent}')
        print(f'The common year of birth: {common_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#-----------------------------------------------------------------------------------

def display_data(df):

    """
    Displays individual trip data from a DataFrame in a paginated manner.

    This function prompts the user to view rows of trip data in a paginated format,
    showing 5 rows at a time. The user can continue to view additional rows by
    responding 'yes' to the prompt.
    """
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)  

        restart = input('\nWould you like to restart? Enter yes or no: ').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()






