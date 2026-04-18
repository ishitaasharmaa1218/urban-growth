import folium
from streamlit_folium import folium_static

def show_map(df):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=row['city'],
            color='red',
            fill=True
        ).add_to(m)

    return m