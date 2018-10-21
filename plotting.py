import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from textblob import TextBlob

def sightings_when(df):
    '''
    Analyzes when the most sightings occur, and creates a bar plot of sightings over time(per year)
    :param df: Dataframe holding UFO statistics
    :return: Plot and string, telling the month of most sightings
    '''
    sightings_by_year = df['Datetime'].dt.year.value_counts().to_dict()
    sightings_by_month = df['Datetime'].dt.month.value_counts().to_dict()

    dates = list(sightings_by_year.keys())
    sightings = list(sightings_by_year.values())

    plt.bar(dates, sightings, width=0.5, linewidth=1, align='center')
    plt.axis([min(dates), max(dates), 0, max(sightings) + 10])
    plt.title('Distribution of sightings over time', fontsize=12)
    plt.xlabel("Year", fontsize=10)
    plt.ylabel("Sightings", fontsize=10)

    month_most = next(iter(sightings_by_month.keys()))
    month_most = datetime(1900, month_most, 1).strftime('%B')

    sightings_answer = 'The most sightings happen during ' + month_most

    return plt, sightings_answer

def dayoftheweek(df):
    '''
    Calculates the distribition of UFO sightings based on weekday, and plots this into a scatter plot.
    :param df: Dataframe holding UFO statistics
    :return: Returns a plot showing this & a list holding number of sightings per day - index as weekday
    '''
    dow = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    sightings_by_day = df['Datetime'].dt.dayofweek.value_counts().to_dict()

    sbd = [None] * 7
    for key, item in sightings_by_day.items():
        sbd[int(key)] = float(item)

    sbd_total = sum(sbd)
    sbd_prc = [round(((item / sbd_total) * 100), 2) for item in sbd]

    plt.clf()
    plt.scatter(dow, sbd_prc)

    plt.title('Days of the Week to spot a UFO', fontsize=12)
    plt.xlabel("Weekday", fontsize=10)
    plt.ylabel("Percentage of sightings", fontsize=10)

    return plt, sbd


def sentiment_analyzis(df, nm='sub'):
    '''
    Analyzes the co-relation between the Subjectivty of a sentence and it's polarity, using Sentiment Analyzis
    :param df: Dataframe holding UFO statistics
    :param nm: Normalize - determines wheter to normalize on subjectivity or Polarity
    :return: A plot showing Subjectivty and Polarity sighting by sighting & a zoom view of the same plot
    '''

    subjectivity = []
    polarity = []
    lby = ''

    for row in df.itertuples():
        comment = TextBlob(str(getattr(row, "Comments")))
        p, s = comment.sentiment


        if nm == 'pol':
            lby = 'Polarity Normalized'
            subjectivity.append(s)

            if p < 0.0:
                polarity.append(0.0)
            else:
                polarity.append(p)

        if nm == 'sub':
            lby = 'Subjectivity Normalized'
            polarity.append(p)
            if s > 0.5:
                subjectivity.append((s - 0.5) * 2)
            else:
                subjectivity.append((s * -2))

    r_patch = mpatches.Patch(color='red', label='Subjectivity')
    g_patch = mpatches.Patch(color='green', label='Polarity')

    plot1 = plt.figure()

    plt.clf()
    plt.plot(subjectivity, c='red', linewidth=0.01)

    plt.title("Sentiment Analyzis", fontsize=20)
    plt.xlabel("Observations", fontsize=12)
    plt.ylabel(lby, fontsize=12)
    plt.plot(polarity, c='green', linewidth=0.01)

    plt.tick_params(axis='both', labelsize=10)
    plt.legend(handles=[g_patch, r_patch], loc='upper right', prop={'size': 10})

    plot2 = plt.figure()

    plt.clf()
    plt.plot(subjectivity[-100:], c='red', linewidth=0.5, label='Subjectivity')

    plt.title("Sentiment Analyzis(fragment)", fontsize=20)
    plt.xlabel("Observations", fontsize=12)
    plt.ylabel(lby, fontsize=12)
    plt.plot(polarity[-100:], c='green', linewidth=0.5)

    plt.tick_params(axis='both', labelsize=10)
    plt.legend(handles=[g_patch, r_patch], loc='upper right', prop={'size': 10})

    return plot1, plot2