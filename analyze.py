from datahandler import states
import matplotlib.pyplot as plt
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

    fig = plt.figure()

    month_most = next(iter(sightings_by_month.keys()))
    month_most = datetime(1900, month_most, 1).strftime('%B')

    print('The most sightings happen during', month_most)

    return fig, sightings_by_month, sightings_by_year


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