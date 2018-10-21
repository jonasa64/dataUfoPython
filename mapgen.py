import pandas as pd
import folium
from states import states_us

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