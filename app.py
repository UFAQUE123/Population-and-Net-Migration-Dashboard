   
   # Population and Net Migration Dashboard
   

# import libraries
import streamlit as st
import wbdata
import pandas as pd
import plotly.express as px

# Load the data
indicator = {
    'SP.POP.TOTL': 'total_population',  # Population
    'SM.POP.NETM': 'net_migration'     # Net Migration
}

data = wbdata.get_dataframe(indicator)
data.reset_index(inplace=True)
data.rename(columns={'country': 'Country', 'date': 'Year'}, inplace=True)
data['Year'] = pd.to_numeric(data['Year'])
data = data[(data['Year'] >= 1960) & (data['Year'] <= 2025)]

st.title("📊 Population and Net Migration Dashboard")
st.subheader(''' 
             Analyzing Global Population Trends and Migration Patterns with Interactive Visuals
             ''')
st.divider()
st.sidebar.header("Filters")

# Country Selection
selected_countries = st.sidebar.multiselect("Select Countries:",
                                            data["Country"].unique(), 
                                            default=["Pakistan"])

# Year Range Selection
min_year, max_year = int(data["Year"].min()), int(data["Year"].max())
year_range = st.sidebar.slider("Select Year Range:", 
                               min_value=min_year,
                               max_value=max_year, 
                               value=(2015, 2025))

# Filter data
filtered_data = data[(data["Country"].isin(selected_countries)) & (data["Year"].between(year_range[0],
                                                                                        year_range[1]))]

# Assigning tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Total Population Over Years",
    "🌍 Net Migration Over Years",
    "📊 Population Comparison for Selected Year & Countries",
    "🔄 Net Migration vs. Total Population",
    "🏆 Top 10 Most Populous Countries",
    "🚀 Top 10 Countries by Net Migration Rate"
])

with tab1:
        # Plot Total Population
        fig_pop = px.line(filtered_data, x="Year",
                  y="total_population", 
                  color="Country", 
                  title="📈 Total Population Over Years")
        st.plotly_chart(fig_pop)

with tab2:
        # Plot Net Migration
        fig_migration = px.line(filtered_data, 
                        x="Year", 
                        y="net_migration", 
                        color="Country", 
                        title="🌍 Net Migration Over Years")
        st.plotly_chart(fig_migration)

with tab3:
        # Sidebar: Select Year & Countries
        selected_year = st.sidebar.slider("Select a Year for Comparison:", 
                                  min_value=min_year, 
                                  max_value=max_year, 
                                  value=2020)

        selected_countries = st.sidebar.multiselect("Select Countries for Comparison:", 
                                            data["Country"].unique(), 
                                            default=["Pakistan", "India", "Bangladesh"])

         # Filter data based on selection
        yearly_data = data[(data["Year"] == selected_year) & (data["Country"].isin(selected_countries))]

         # Sidebar: Theme Toggle
        theme = st.sidebar.radio("Select Theme:", ["Light Mode", "Dark Mode"])
        theme_color = "plotly_dark" if theme == "Dark Mode" else "plotly"

         # Bar Chart: Population Comparison for Selected Year & Countries
        fig_bar = px.bar(yearly_data, x="Country", y="total_population", color="Country",
                 title=f"📊 Population Comparison for {selected_year}", 
                 template=theme_color)
        st.plotly_chart(fig_bar, use_container_width=True)
        
with tab4:
        # Scatter Plot
        fig_scatter = px.scatter(filtered_data,
                         x="net_migration", 
                         y="total_population", 
                         color="Country",
                         hover_data=["Year","net_migration","total_population","Country"],
                         title=f"🔄 Net Migration vs. Total Population ({year_range[0]}–{year_range[1]})",
                         size="total_population")
        st.plotly_chart(fig_scatter)
        
with tab5:
        # Show Top 5 Countries 
        selected_year_1 = st.sidebar.slider("Select a Year for top 5 Countries Comparison:", 
                                  min_value=min_year,
                                  max_value=max_year,
                                  value=2002)
        yearly_data_1 = data[data["Year"] == selected_year_1]
        st.subheader(f"🏆 Top 10 Most Populous Countries in {selected_year_1}")
        top_countries = yearly_data_1.nlargest(10, "total_population")[["Country", "total_population"]]
        st.dataframe(top_countries)
      
with tab6:
        # Show Top 5 Countries by Migration
        st.subheader(f"🚀 Top 10 Countries by Net Migration Rate in {selected_year_1}")
        top_migration = yearly_data_1.nlargest(10, "net_migration")[["Country", "net_migration"]]
        st.dataframe(top_migration)


## conda environment name is: population
