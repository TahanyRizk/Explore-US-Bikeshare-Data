import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington?\n')
    city=city.lower()
    if city not in ["chicago", "new york", "washington"]:
        print('not a valid city')
        city, month, day="","",""
        return city, month, day

    answer=input('Would you like to filter the data by month, day, or not at all ? type non for no time filter \n')

    # get user input for month (all, january, february, ... , june)
    if answer.lower() == 'month':
        month=input('Which month - January, February, March, April, May, or June?\n')
        day=""
        month=month.lower()
        ##if month not in ["January", "February", "March", "April", "May", "June"]:
        if month not in map(str.lower,["January", "February", "March", "April", "May", "June"]):
            print('not a valid month')
            city, month, day="","",""
            return city, month, day

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif answer.lower() == 'day':
        day=input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
        month=""
        day=day.lower()
        ##if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        if day not in map(str.lower,["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
            print('not a valid day')
            city, month, day="","",""
            return city, month, day

    elif answer.lower() == 'non':
        month, day="all","all"

    else:
        print('not a valid answer, you dont give a correct choice')
        city, month, day="","",""

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
    try:
        df = pd.read_csv(CITY_DATA[city])
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        # filter by month if applicable
        if month != 'all'  and month != "":
        # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            # filter by month to create the new dataframe
            df = df[df['month'] == month]
            print(df['month'].value_counts())

        # filter by day of week if applicable
        if day != 'all' and day != "":
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
            print(df['day_of_week'].value_counts())

    except Exception as e:
        print("Exception occurred: {}".format(e))
        return pd.DataFrame()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    try:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        if 'month' not in df.columns:
            df['month'] = df['Start Time'].dt.month

        popular_month =df['month'].mode() [0]
        popular_month_count=len(df[df['month'] == popular_month])

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month_name = months[popular_month - 1]

        # display the most common day of week
        if 'day_of_week' not in df.columns:
            df['day_of_week'] = df['Start Time'].dt.day_name()

        popular_day_of_week =df['day_of_week'].mode() [0]
        popular_day_of_week_count=len(df[df['day_of_week'] == popular_day_of_week])


        # display the most common start hour
        df['hour'] =df['Start Time'].dt.hour
        popular_hour =df['hour'].mode() [0]
        popular_hour_count=len(df[df['hour'] == popular_hour])

        print("most common month: "+str(popular_month_name) + " ,     count : "+str(popular_month_count))
        print("most common day_of_week: "+str(popular_day_of_week)+ " ,     count : "+str(popular_day_of_week_count))
        print("most common hour: "+str(popular_hour)+ " ,     count : "+str(popular_hour_count))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    except Exception as e:
        print("Exception occurred: {}".format(e))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    try:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()
        # display most commonly used start station
        common_start_station=df['Start Station'].mode() [0]
        common_start_station_count=len(df[df['Start Station'] == common_start_station])
        print("most commonly used start station is    : "+str(common_start_station)+ " ,     count : "+str(common_start_station_count))

        # display most commonly used end station
        common_end_station=df['End Station'].mode() [0]
        common_end_station_count=len(df[df['End Station'] == common_end_station])
        print("most commonly used end station is    : "+str(common_end_station)+ " ,     count : "+str(common_end_station_count))

        # display most frequent combination of start station and end station trip
        df['combination']='from : '+df['Start Station']+'  to : ' +df['End Station']
        common_combination=df['combination'].mode() [0]
        common_combination_count=len(df[df['combination'] == common_combination])
        print("most common trip from start to end is    : "+str(common_combination)+ " ,     count : "+str(common_combination_count))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except Exception as e:
        print("Exception occurred: {}".format(e))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        # display total travel time
        print("The total travel time is    : "+str(df['Trip Duration'].sum()))
        # display mean travel time
        print("The Average travel time is    : "+str(df['Trip Duration'].mean()))

    except Exception as e:
        print("Exception occurred: {}".format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types: ')
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    if 'Gender'  in df.columns:
        print('\n Counts of Gender : ')
        print(df['Gender'].value_counts())
    else:
        print('No Gender data Available for this City')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year'  in df.columns:
        print("\nearliest year of birth is    : "+str(df['Birth Year'].min()).split('.')[0])
        print("most recent year of birth is    : "+str(df['Birth Year'].max()).split('.')[0])
        print("most common year of birth is    : "+str(df['Birth Year'].mode()[0]).split('.')[0])
    else:
        print('No Birth Year data Available for this City')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_rawdata(city):
    try:
        df1 = pd.read_csv(CITY_DATA[city])
        i=0
        while True and i < df1.shape[0]:
            display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if display_data.lower() != 'yes':
                break
            print(tabulate(df1.iloc[np.arange(0+i,5+i)], headers ="keys"))
            i+=5
    except Exception as e:
        print("Exception occurred: {}".format(e))

    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        #print(city+month+day)

        if city !="":
            df = load_data(city, month, day)
            if not df.empty:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                display_rawdata(city)




        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
