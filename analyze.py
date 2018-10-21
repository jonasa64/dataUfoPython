from datahandler import states, states_us
from datetime import timedelta
from textblob import TextBlob
from random import choice

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




