import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="India Comprehensive Data Dashboard",
    layout='wide',
    initial_sidebar_state='expanded'
)


st.markdown("""
<style>
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
h1, h2 {
    animation: fadeIn 3s ease-in;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #1e272e;
}

/* Sidebar headings & labels text color */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] .css-1d391kg {
    color: white !important;
}


/* Make selectbox text black */
section[data-testid="stSidebar"] .stSelectbox div[role="combobox"] {
    color: black !important;
}

/* set dropdown options text to black */
section[data-testid="stSidebar"] .stSelectbox div[role="listbox"] span {
    color: black !important;
}

/* Main page background */
[data-testid="stAppViewContainer"] > .main {
    background-color: #f5f6fa;
}

/* Button styling */
div.stButton > button {
    color: white;
    background-color: #e67e22;
    border: none;
    padding: 0.6em 1.2em;
    border-radius: 8px;
    font-size: 16px;
    margin-top: 0.5em;
    transition: 0.3s;
}

/* Button hover effect */
div.stButton > button:hover {
    background-color: #d35400;
    transform: scale(1.02);
}
/* Make ALL radio labels text white */
section[data-testid="stSidebar"] .stRadio > div > label > div {
    color: white !important;
}
/* Make download button label text white */
section[data-testid="stSidebar"] .stDownloadButton label span {
    color: white !important;
}
/* Make checkbox labels text white */
section[data-testid="stSidebar"] .stCheckbox > label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)



df = pd.read_csv('india.csv')


list_of_states = list(df['State'].unique())
list_of_states.insert(0, 'Overall India')

# Page title
st.title("📊 India Comprehensive Data Dashboard")
st.markdown("Explore district-wise and state-wise data with interactive visualizations.")

# Sidebar
st.sidebar.header("🛠️ Filters & Controls")

selected_state = st.sidebar.selectbox('Select a State', list_of_states)
primary = st.sidebar.selectbox('Select Primary Parameter', sorted(df.columns[6:]))
secondary = st.sidebar.selectbox('Select Secondary Parameter', sorted(df.columns[6:]))


# Extra controls
map_style = st.sidebar.radio(
    "Select Map Style",
    options=["open-street-map", "carto-positron", "carto-darkmatter"],
    index=0
)

show_table = st.sidebar.checkbox("Show Data Table Below Map", value=True)


# Download CSV
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Full Data as CSV",
    data=csv,
    file_name='india_data.csv',
    mime='text/csv',
)


plot = st.sidebar.button('Plot Graph')


if plot:

    st.markdown(f"**Size represents:** `{primary}` &nbsp;&nbsp; | &nbsp;&nbsp; **Color represents:** `{secondary}`")
    st.markdown("---")

    if selected_state == 'Overall India':
        fig = px.scatter_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            size=primary,
            color=secondary,
            zoom=4,
            center={"lat": 22.5, "lon": 80},
            size_max=35,
            mapbox_style=map_style,
            color_continuous_scale="turbo",
            width=1200,
            height=700,
            hover_name='District'
        )

        fig.update_traces(marker=dict(opacity=0.85))
        st.plotly_chart(fig,
        use_container_width=False,
        config={
            "scrollZoom": True,
            "displayModeBar": True,
            "responsive": False
        })

        if show_table:
            st.subheader("Full Data Table")
            st.dataframe(df)

    else:
        state_df = df[df['State'] == selected_state]
        fig = px.scatter_mapbox(
            state_df,
            lat="Latitude",
            lon="Longitude",
            size=primary,
            color=secondary,
            zoom=5,
            center={
                "lat": state_df['Latitude'].mean(),
                "lon": state_df['Longitude'].mean()
            },
            size_max=35,
            mapbox_style=map_style,
            color_continuous_scale="turbo",
            width=1200,
            height=700,
            hover_name='District'
        )
        fig.update_traces(marker=dict(opacity=0.85))
        st.plotly_chart(fig,
        use_container_width=False,
        config={
            "scrollZoom": True,
            "displayModeBar": True,
            "responsive": False
        })

        if show_table:
            st.subheader(f"{selected_state} Data Table")
            st.dataframe(state_df)

    st.markdown("""
    ---
    ### ✨ Insights & Tips

    - **Bubble Size**: Larger bubbles represent higher values of the **Primary Parameter** you selected.
    - **Color Gradient**: Colors indicate variation in the **Secondary Parameter**. Notice patterns or outliers.
    - **Map Styles**: Experiment with different map styles for better readability or aesthetics.
    - **Zoom & Pan**: You can zoom and drag the map to focus on specific regions or districts.
    - **Data Table**: Toggle the data table below the map to view exact figures for all districts.

    """)

    st.markdown("""
    <hr style="margin-top:2em;">
    <div style="text-align:center; color:green;">
    #✨# Made by Rohit Ranjan | Streamlit & Plotly #✨#
    </div>
    """, unsafe_allow_html=True)