from datahandler import states, states_us
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
from textblob import TextBlob
from random import choice

def sightings_where(df):
    sightings_by_city = df['City'].value_counts().to_dict()
    sightings_by_state = df['State'].value_counts().to_dict()

    city_most = next(iter(sightings_by_city.keys()))
    state_most = next(iter(sightings_by_state.keys()))

    print(city_most.title(), 'is the city with the most UFO sightings. (' + str(sightings_by_city[city_most]) + ' sightings)')
    print(states[state_most.upper()], 'is the state with the most UFO sightings.(' + str(sightings_by_state[state_most]) + ') sightings')

    return sightings_by_city, sightings_by_state


def sightings_when(df):
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

    print('The most sightings happen during', month_most)

    return plt, sightings_by_month, sightings_by_year


def appearance(df):
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
            wd = str(word.define())
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

    print("It seems that UFO's often appear", choice(shapes), "shaped and", choice(colors))

    return shapes, colors

def duration(df):
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

    print("The average UFO-sighting lasted", delta_string)

    return delta_string


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
            lb = 'Polarity Normalized'
            subjectivity.append(s)

            if p < 0.0:
                polarity.append(0.0)
            else:
                polarity.append(p)

        if nm == 'sub':
            lb = 'Subjectivity Normalized'
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

    plt.title("Sentiment Analyzis", fontsize=20)
    plt.xlabel("Observations", fontsize=12)
    plt.ylabel(lby, fontsize=12)
    plt.plot(polarity[-100:], c='green', linewidth=0.5)

    plt.tick_params(axis='both', labelsize=10)
    plt.legend(handles=[g_patch, r_patch], loc='upper right', prop={'size': 10})

    return plot1, plot2

def state_map_plot(df):
    sightings_by_state = df['State'].value_counts().to_dict()
    blue_offset = 20
    r = hex(0)
    g = hex(0)
    b = hex(blue_offset)

    total_states = len(states_us)
    color_increment = (int('ff', base=16) - blue_offset) / total_states

    color_count_mapping = []

    i = 0
    for key, value in sightings_by_state.items():
        if key.upper() in states_us:
            i += 1
            color = '#0000' + b[2:].zfill(2)
            b = float(blue_offset) + color_increment * float(i)
            b = hex(int(b))

            color_count_mapping.append((key, states_us[key.upper()], value, color))