from datahandler import states
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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

#Hvordan ser en ufo ud?

#Find flere buzzwords som f.eks. form, farve eller andet. Her kan det være en fordel at bruge textBlob. https://textblob.readthedocs.io/en/dev/


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

    print("An average UFO-sighting lasted", delta_string)

    return delta_string