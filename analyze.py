from datahandler import states, states_us
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
from random import choice
import folium

# state and city with most UFO's
def sightings_where(df):
    #Convert the DataFrame to a dictionary 
    sightings_by_city = df['City'].value_counts().to_dict()
    sightings_by_state = df['State'].value_counts().to_dict()
    #Retrieve the next item from the iterator 
    city_most = next(iter(sightings_by_city.keys()))
    state_most = next(iter(sightings_by_state.keys()))
     # most city
    city_answer = city_most.title() + ' is the city with the most UFO sightings. (' + str(sightings_by_city[city_most]) + ' sightings)'
    #most state 
    state_answer = states[state_most.upper()] + ' is the state with the most UFO sightings.(' + str(sightings_by_state[state_most]) + ') sightings'

    return city_answer, state_answer

# when most UFO are seen
def sightings_when(df):
       #Convert the DataFrame to a dictionary 
    sightings_by_year = df['Datetime'].dt.year.value_counts().to_dict()
    sightings_by_month = df['Datetime'].dt.month.value_counts().to_dict()

    dates = list(sightings_by_year.keys())
    sightings = list(sightings_by_year.values())

    plt.bar(dates, sightings, width=0.5, linewidth=1, align='center')
    plt.axis([min(dates), max(dates), 0, max(sightings) + 10])
    plt.title('Distribution of sightings over time', fontsize=12)
    plt.xlabel("Year", fontsize=10)
    plt.ylabel("Sightings", fontsize=10)
      #Retrieve the next item from the iterator 
    month_most = next(iter(sightings_by_month.keys()))
    month_most = datetime(1900, month_most, 1).strftime('%B')

    sightings_answer = 'The most sightings happen during ' + month_most

    return plt, sightings_answer


def appearance(df):
    #Empty dict for shap and color 
    shape_dict = {}
    color_dict = {}
    #the itertuples Iterate over DataFrame rows as namedtuples, with index value as first element of the tuple
    for row in df.itertuples():
        tempshape = set()
        tempcolor = set()
        shape = str(getattr(row, "Shape")).split()
        for word in shape:
            tempshape.add(word.lower())

        blob = TextBlob(" ".join(str(getattr(row, "Comments")).split("/")))

        for word in blob.sentences[0].words:
            wd = str(word.define())
            if 'shape' in wd:
                tempshape.add(word.lower())
            if 'color' in wd:
                tempcolor.add(word.lower())

        for word in tempshape:
            if 'shape' not in word:
                #setdeault take a key to be searched in the dictionary as first Parameters and default_value there are optional
                shape_dict.setdefault(word, 0)
                shape_dict[word] += 1

        for word in tempcolor:
            if 'color' not in word:
                color_dict.setdefault(word, 0)
                color_dict[word] += 1
     #sort the list whit the shape and color 
    shapes = list(sorted(shape_dict, key=shape_dict.__getitem__))
    colors = list(sorted(color_dict, key=color_dict.__getitem__))

    shapes = shapes[-10:]
    colors = colors[-10:]

    appearance_answer = "It seems that UFO's often appear " + choice(shapes) + " shaped and " + choice(colors)

    return appearance_answer

def duration(df):
    #mean() function used to calculate mean/average of a given list of numbers
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
    # clf() Clear the current figure.
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
