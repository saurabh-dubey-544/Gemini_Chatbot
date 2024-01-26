import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from helper import overall_population , preprocess
from functions import overall_data,num_countries,list_of_countries,pie_trade,fertility_rate,IMR,pop_reg,region_trade,region_trade_perc,reg_fer_rate,country_wise_analysis,age_class


df = pd.read_csv('Web_app\dataset\country_variables.csv')

df = preprocess(df)

# st.header('Countries Profile Analysis')

st.sidebar.title('Countries Analysis')

user_menu = st.sidebar.radio(
    "Select an option",
    ("Overall Analysis" , "Region-wise Analysis" , 'Country-wise Analysis')
)


# Overall Analysis
if user_menu == 'Overall Analysis':
    
    select_analysis = st.sidebar.selectbox("Chose an option" , ["Overall" , "Top Statistics"])
    if select_analysis == 'Overall':
    
        st.title("Overall Analysis")
        # Tab version
        overall,population,surface_area,gdp,economy,demographics = st.tabs(["Overall","Population","Surface_area","GDP","Economy","Demographics"])
        
        # Overall tab
        over_df = overall_data(df)
        
        overall.table(over_df)
        
        
        # Population tab
        population.header("Top 5 Populated countries")
        top_pop = df[['country' , 'Population (2017)']].sort_values(by='Population (2017)' , ascending=False).head()
        population.table(top_pop)
        
        population.header("Least 5 Populated Countries")
        least_pop = df[['country' , 'Population (2017)']].sort_values(by='Population (2017)' , ascending=True).head()
        population.table(least_pop)

        population.header("Population Density(Top5)")
        top_den = df[['country' , 'Population density (per km2, 2017)']].sort_values(by='Population density (per km2, 2017)' , ascending=False).head()
        population.table(top_den)
        
        population.header("Population Density(Least5)")
        least_den = df[['country' , 'Population density (per km2, 2017)']].sort_values(by='Population density (per km2, 2017)' , ascending=True).head()
        population.table(least_den)
        
        # Surface area tab
        surface_area.header("Largest countries (in terms of Surface area)")
        top5 = df[['country','Surface area (km2)']].sort_values(by='Surface area (km2)' ,ascending=False).head()
        surface_area.table(top5)
        
        surface_area.header("Smallest countries (in terms of Surface area)")
        least5 = df[['country','Surface area (km2)']].sort_values(by='Surface area (km2)' ,ascending=True).head()
        surface_area.table(least5)
    
        # GDP tab
        # GDP
        gdp.header("Top 5 GDP")
        top5 = df[['country','GDP: Gross domestic product (million current US$)']].sort_values(by='GDP: Gross domestic product (million current US$)' , ascending=False).head()
        gdp.table(top5)
        
        # GDP per capita
        gdp.header("Top 5 GDP per capita")
        top5 = df[['country' ,'GDP per capita (current US$)']].sort_values(by = 'GDP per capita (current US$)' , ascending=False).head()
        gdp.table(top5)
        
        gdp.header("Least 5 GDP per capita")
        least5 = df[['country' ,'GDP per capita (current US$)']].sort_values(by = 'GDP per capita (current US$)' , ascending=True).head()
        gdp.table(least5)
        
        # Economy
        economy.header("Economy & Trade")
        agr = df['Economy: Agriculture (% of GVA)'].mean()
        ind = df['Economy: Industry (% of GVA)'].mean()
        ser = df['Economy: Services and other activity (% of GVA)'].mean()
        fig = px.pie(values=[agr , ind , ser], names=['Agriculture' , 'Industry' , 'Services'], title="Distribution of world's Economy")
        economy.plotly_chart(fig)
            
        # --World Trade--
        economy.header("World's Trade Distribution")
        economy.plotly_chart(pie_trade(df))
        
        # Demographics
        demographics.header("Fertility rates")
        top5,least5 = fertility_rate(df)
        demographics.write("Highest Fertility rates")
        demographics.table(top5)
        demographics.write("Lowest Fertility rates")
        demographics.table(least5)

        demographics.header("Infant Mortality Rate")
        top5,least5 = IMR(df)
        demographics.write("Highest Infant Mortality Rate")
        demographics.table(top5)
        demographics.write("Lowest Infant Mortality Rate")
        demographics.table(least5)
        
        
            
if user_menu == "Region-wise Analysis":
    
    demographics,trade = st.tabs(["Demographics","Trade"])
    
    # Demographics
    demographics.header("Region-wise Countries Distribution")
    fig = num_countries(df)
    demographics.plotly_chart(fig)
    
    demographics.header("Region-wise Population distribution")
    fig = pop_reg(df)
    demographics.plotly_chart(fig)
    
    demographics.header("Region-wise Fertility Rate")
    fig = reg_fer_rate(df)
    demographics.plotly_chart(fig)
    
    # Trade
    trade.header("Region-wise Trade Contribution")
    fig = region_trade(df)
    trade.plotly_chart(fig)
    
    trade.header("Region-wise Percentage trade")
    fig = region_trade_perc(df)
    trade.plotly_chart(fig)
    

    
if user_menu == 'Country-wise Analysis':
    countries = list_of_countries(df)
    
    country = st.sidebar.selectbox(label="Chose any Country" , options=countries)
    df1 = df[df['country'] == country]
    loc,pop,gdp,gdp_pc,sr,urb_pop,urb_gr,fer_rat,imr,fig_econ,fig_trad,fig_emp,table,fig_lif,fig_lab = country_wise_analysis(df1)
    st.title("Information about" + " "+ country)
    col1,col2 = st.columns(2)
    
    
    col1.header("Basic Information about" + " "+ country)
    col1.table(table)
    
    col2.header("Economy Distribution of" + " "+ country)
    fig = fig_econ
    col2.plotly_chart(fig)
    col1,col2 = st.columns(2)
    col1.header("Trade Distribution of" + " "+ country)
    fig = fig_trad
    col1.plotly_chart(fig)
    col2.header("Employment in different sectors in" + " "+ country)
    fig = fig_emp
    col2.plotly_chart(fig)
    col1,col2 = st.columns(2)
    col1.header("Labor Force participation Men vs Women in" + " "+ country)
    col1.plotly_chart(fig_lab)
    col2.header("Life Expectancy Males vs Females in" + " "+ country)
    col2.plotly_chart(fig_lif)
    col1,col2 = st.columns(2)
    col1.header("Age-class Distribution of" + " " + country)
    fig = age_class(df1)
    st.plotly_chart(fig)
    