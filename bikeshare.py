import time
import calendar
import pandas as pd

#create possible user entries for the data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#create list of months:
months = ['all','january','february', 'march', 'april', 'may', 'june']

#create list of weekdays
weekdays = list(calendar.day_name)
weekdays_lower = [weekdays_lower.lower() for weekdays_lower in weekdays]
weekdays_lower.append('all')

#Check for valid input
def valid_input (message, inputs):
    """
    Parameters
    ----------
    message : (str) - dialog displayed to the user
    inputs : (list) - list of valid inputs

    Returns
    -------
    response : (str) - valid user intput
    """

    while True:
        response = input(message).lower()
        if response in inputs:
            return response

        elif response == "new york":
            response = "new_york_city"
            return response

        else:
            print("This is not a valid input, please try again")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = valid_input("Please enter a city out of the options 'Chicago', 'New York City' "
                      "and 'Washington': ",list(CITY_DATA.keys()))
    if city == "new york city":
        city = "new_york_city"

    # get user input for month (all, january, february, ... , june)
    month = valid_input("Please enter a month out of the options 'all', 'january' "
                        ", 'february', 'march', 'april', 'may', 'june': ",months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = valid_input("Please enter a weekday out of the options"
                      " 'all','monday',...,'sunday': ",weekdays_lower)

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
    #read raw data as csv
    df = pd.read_csv(city + ".csv")

    #change Timedata in dtaframe to datetime time for better processing
    #use Start time column to extract months and days of rental events
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #create column of month names by extracting from Start Time
    #to be able to filter after month
    df['month'] = df['Start Time'].dt.month_name()

    #create column of month names by extracting from Start Time
    #to be able to filter after month
    df['day'] = df['Start Time'].dt.day_name()


    #filter by month
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month']==month.capitalize()]

    #filter by day
    if day != 'all':
        # filter by day to create the new dataframe
        df = df[df['day']==day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most frequent month is:\n')
    print(df.month.mode().loc[0] + '\n')

    # display the most common day of week
    print('The most frequent day is:\n')
    print(df.day.mode().loc[0] + '\n')

    # display the most common start hour
    print('The most common start hour is:\n')
    print(df['Start Time'].dt.hour.mode().loc[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used Start Station is: \n\n{}\n"
          .format(df['Start Station'].mode().loc[0]))

    print("\nIt appears {} times in the data."
          .format(df['Start Station'].value_counts().head(1).mode().loc[0]))

    # display most commonly used end station
    print("\nThe most commonly used End Station is: \n\n{}\n"
          .format(df['End Station'].mode().loc[0]))
    print("\nIt appears {} times in the data."
          .format(df['End Station'].value_counts().head(1).mode().loc[0]))

    # display most frequent combination of start station and end station trip
    start_end = df.groupby(['Start Station', 'End Station'])
    print('\nThe most frequent combination of Start and End Station is: \n')
    print(start_end.size().sort_values(ascending=False).head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # calculate trip duration per trip in minutes
    timediff = (df['End Time'] - df['Start Time']).astype('timedelta64[s]')/60

    #calculate total traveltime in hours
    total_travel_t =timediff.sum()/60

    #round to two decimals:
    total_travel_t= round(total_travel_t,2)
    print('The total travel time is {} hours'.format(total_travel_t))

    # display mean travel time
    #mean travel time in minutes
    mean_travel_t = timediff.mean()

    #round to two decimals
    mean_travel_t = round(mean_travel_t,2)
    print("The mean travel time is {} minutes".format(mean_travel_t))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Usertypes:\n')
    try:
        print(df['User Type'].value_counts())
    except KeyError:
        print('Sorry, no User Type Data in Dataset')

    # Display counts of gender
    print('\nGender:\n')
    try:
        print(df['Gender'].value_counts())
    except KeyError:
        print('Sorry, no Gender Data in Dataset')

    # Display earliest, most recent, and most common year of birth
    print('\nEarliest year of birth:\n')
    try:
        print(int(df['Birth Year'].min()))
    except KeyError:
        print('Sorry no Birth Year Data in Dataset')

    print('\nMost recent year of birth:\n')
    try:
        print(int(df['Birth Year'].max()))
    except KeyError:
        print('Sorry no Birth Year Data in Dataset')


    print('\nMost common year of birth:\n')
    try:
        print(int(df['Birth Year'].mode().iloc[0]))
    except KeyError:
        print('Sorry no Birth Year Data in Dataset')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def show_data (df):
    """
    Shows 5 lines of the given data frame and continues until the user quits
    by typing "no"

    Parameters
    ----------
    df : Dataframe with Bikeshare data of different US cities.

    Returns
    -------
    None.

    """
    
    response = valid_input("Do you wish to see 5 rows of trip data?" +
                     " Please enter yes or no.\n",['yes','no'])
    df_loc = 0 
    
    while True:
        if response == 'yes':
            print(df.iloc[df_loc:df_loc+5])
            df_loc = df_loc+5
        elif response == 'no':
            print("You decided to quit, Good bye!")
            break
        response = valid_input("Do you wish to continue?"
                               + " Yes will show the next 5 lines, no will quit.\n",
                               ['yes','no'])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
