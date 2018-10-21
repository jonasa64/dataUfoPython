from datahandler import states, states_us
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
from random import choice
import folium

def sightings_where(df):
    '''
    Analyzes the most sightings according to location: city & state
    :param df: Dataframe holding UFO statistics
    :return: Two strings, answering this
    '''
    sightings_by_city = df['City'].value_counts().to_dict()
    sightings_by_state = df['State'].value_counts().to_dict()

    city_most = next(iter(sightings_by_city.keys()))
    state_most = next(iter(sightings_by_state.keys()))

    city_answer = city_most.title() + ' is the city with the most UFO sightings. (' + str(sightings_by_city[city_most]) + ' sightings)'
    state_answer = states[state_most.upper()] + ' is the state with the most UFO sightings. (' + str(sightings_by_state[state_most]) + ' sightings)'

    return city_answer, state_answer


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


def appearance(df):
    '''
    Tries to analyze how a UFO looks like, based on buzzwords in comments from the observations
    :param df: Dataframe holding UFO statistics
    :return: A partially random generated string, describing how a UFO might appear
    '''
    shape_dict = {}
    color_dict = {}
    for row in df.itertuples():
        tempshape = set()
        tempcolor = set()
        shape = str(getattr(row, "Shape")).split()
        for word in shape:
            tempshape.add(word.lower())

        blob = TextBlob(" ".join(str(getattr(row, "Comments")).split("/")))

        for word in blob.sentences[0].words:
            wd = str(word.define()).lower()
            if 'shape' in wd:
                tempshape.add(word.lower())
            if 'color' in wd:
                tempcolor.add(word.lower())

        for word in tempshape:
            if 'shape' not in word:
                shape_dict.setdefault(word, 0)
                shape_dict[word] += 1

        for word in tempcolor:
            if 'color' not in word:
                color_dict.setdefault(word, 0)
                color_dict[word] += 1

    shapes = list(sorted(shape_dict, key=shape_dict.__getitem__))
    colors = list(sorted(color_dict, key=color_dict.__getitem__))

    shapes = shapes[-10:]
    colors = colors[-10:]

    appearance_answer = "It seems that UFO's often appear " + choice(shapes) + " shaped and " + choice(colors)

    return appearance_answer

def duration(df):
    '''
    Based on the dataframe, gives an average of the duration of a UFO sighting
    :param df: Dataframe holding UFO statistics
    :return: String answering this
    '''
    duration_delta = str(timedelta(seconds=df['Duration'].mean()))

    duration_delta = duration_delta.split()
    delta_string = duration_delta[-1].split(':')
    delta_string = (
            delta_string[0] + ' hours '
            + delta_string[1] + ' minutes '
            + str(round(float(delta_string[2]))) + ' seconds'
    )

    if len(duration_delta) != 1:
        delta_string = " ".join(duration_delta[0:2]) + " " + delta_string

    duration_answer = "The average UFO-sighting lasted " + delta_string

    return duration_answer


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

def state_map_plot(df):
    '''
    Createa a Chrolopleth map based on the Dataframe, showing the distribution of sightings per state
    :param df: Dataframe holding UFO statistics
    :return: HTML page as string, showing Choropleth map
    '''
    sightings_by_state = df['State'].value_counts().to_dict()
    state_data = []

    for key, value in sightings_by_state.items():
        if key.upper() in states_us:
            st = key.upper()
            state_data.append((st, states_us[st], value))

    m = folium.Map(location=[37, -102], zoom_start=5)
    mapframe = pd.DataFrame(state_data, columns=['StateABB', 'State', 'Sightings'])

    m.choropleth(
        geo_data='us_states.json',
        name='choropleth',
        data=mapframe,
        columns=['StateABB', 'Sightings'],
        key_on='feature.id',
        fill_color='YlOrRd',
        fill_opacity=0.5,
        line_opacity=0.5,
        legend_name='UFO Sightings'
    )

    folium.LayerControl().add_to(m)

    return m.get_root().render()