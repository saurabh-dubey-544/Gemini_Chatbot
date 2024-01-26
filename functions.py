import plotly.express as px
import pandas as pd


def overall_data(df):
    numb_countries = df['country'].nunique()
    num_regions = df['Region'].nunique()
    tot_pop = df['Population (2017)'].sum()
    tot_surf = int(df['Surface area (km2)'].sum())
    
    over_df = pd.DataFrame([numb_countries , num_regions , tot_pop , tot_surf] , index=['Number of Countries' , 'Number of Regions','Total Population' , 'Total Surface area(km2)'] , columns=['Overall Data'])
    
    return over_df


def num_countries(df):
    val_cou = df['Region_combined'].value_counts()
    val_cou = val_cou.reset_index().rename({'index' : "Region" , 'Region_combined':'Number of countries'} , axis=1)
    
    fig = px.pie(val_cou, values='Number of countries', names='Region', title='Number of countries in each region')
    return fig

def list_of_countries(df):
    return df['country'].unique().tolist()

def pie_trade(df):
    trade_perc = df[['country' , 'Overall Trade percentage']].sort_values(by='Overall Trade percentage', ascending=False)
    values = trade_perc.head(10)['Overall Trade percentage'].tolist()
    names = trade_perc.head(10)['country'].tolist()
    others = trade_perc.iloc[10:,:]['Overall Trade percentage'].sum()
    values.append(others)
    names.append("Others")
    
    fig = px.pie(values=values, names=names, title="World Trade Distribution")
    
    return fig


def fertility_rate(df):
    top5 = df[['country','Fertility rate, total (live births per woman)']].sort_values(by='Fertility rate, total (live births per woman)',ascending=False).head()
    least5 = df[['country','Fertility rate, total (live births per woman)']].sort_values(by='Fertility rate, total (live births per woman)',ascending=True).head()
    
    return top5,least5

def IMR(df):
    top5 = df[['country','Infant mortality rate (per 1000 live births']].sort_values(by='Infant mortality rate (per 1000 live births',ascending=False).head()
    least5 = df[['country','Infant mortality rate (per 1000 live births']].sort_values(by='Infant mortality rate (per 1000 live births',ascending=True).head()
    
    return top5,least5

def pop_reg(df):
    pop = df[['country' , 'Region_combined' , 'Population (2017)']].groupby('Region_combined').mean().sort_values(by='Population (2017)' , ascending=False)
    pop = pop.reset_index()
    values=pop['Population (2017)'].tolist()
    names = pop['Region_combined'].tolist()
    fig = px.pie(values=values , names=names , title="Distribution of Population Region-wise")
    
    return fig
        
def region_trade(df):
    x = df[['Region_combined','Overall Trade(million US$)']].groupby('Region_combined').sum().reset_index().sort_values(by='Overall Trade(million US$)',ascending=False)
    fig = px.bar(x, y='Region_combined', x='Overall Trade(million US$)')
    return fig

def region_trade_perc(df):
    x = df[['Region_combined','Overall Trade percentage']].groupby('Region_combined').sum().reset_index().sort_values(by='Overall Trade percentage',ascending=False)
    values = x['Overall Trade percentage'].tolist()
    names = x['Region_combined'].tolist()
    fig = px.pie(values=values, names=names, title="Region-wise Trade percentage")    
    return fig

def reg_fer_rate(df):
    data = df[['Region_combined','Fertility rate, total (live births per woman)']].groupby('Region_combined').mean().reset_index().sort_values(by='Fertility rate, total (live births per woman)')
    fig = px.bar(data, y='Region_combined', x='Fertility rate, total (live births per woman)')
    return fig

def country_wise_analysis(df1):
    # df1 = df[df['country'] == country]
    # Location
    loc = df1['Region_combined'].values[0]
    # Population
    pop = df1['Population (2017)'].values[0]
    # GDP
    gdp = df1['GDP: Gross domestic product (million current US$)'].values[0]
    # GDP per capita
    gdp_pc = df1['GDP per capita (current US$)'].values[0]
    # Sex-ratio
    sr = df1['Sex ratio (m per 100 f, 2017)'].values[0]
    # Urban pop and growth
    urb_pop = df1['Urban population (% of total population)'].values[0]
    # Urban growth
    urb_gr = df1['Urban population growth rate (average annual %)'].values[0]
    # Fertility rate
    fer_rat = df1['Fertility rate, total (live births per woman)'].values[0]
    # Life Exp--Bar chart
    lif_mal = df1['Life_expectancy_males'].values[0]
    lif_fem = df1['Life_expectancy_females'].values[0]
    
    import plotly.graph_objects as go

    # Life expectancy data
    life_expectancy = [lif_mal, lif_fem]

    # Categories
    categories = ['Males', 'Females']

    # Define colors for males and females
    colors = ['royalblue', 'salmon']

    # Create a bar trace for males and females with different colors
    trace = go.Bar(x=categories, y=life_expectancy)

    # Create a figure and add the trace
    fig_lif = go.Figure(data=[trace])

    # Update layout
    fig_lif.update_layout(
        title='Comparison of Life Expectancy by Gender',
        xaxis_title='Gender',
        yaxis_title='Life Expectancy'
    )

    # IMR
    imr = df1['Infant mortality rate (per 1000 live births'].values[0]
    # Labor force participation--Bar chart
    lab_mal = df1['Labour force participation (male)%'].values[0]
    lab_fem = df1['Labour force participation (female)%'].values[0]
    # Economy--pie chart
    agr = df1['Economy: Agriculture (% of GVA)'].values[0]
    ind = df1['Economy: Industry (% of GVA)'].values[0]
    ser = df1['Economy: Services and other activity (% of GVA)'].values[0]
    fig_econ = px.pie(values=[agr,ind,ser],names=['Agriculture','Industry','Services'])
    # Trade
    exp = df1['International trade: Exports (million US$)'].values[0]
    imp = df1['International trade: Imports (million US$)'].values[0]
    fig_trad = px.pie(values=[exp,imp] , names=['Export' , 'Import'])
    # Employment--pie
    emp_agr = df1['Employment: Agriculture (% of employed)'].values[0]
    emp_ind = df1['Employment: Industry (% of employed)'].values[0]
    emp_ser = df1['Employment: Services (% of employed)'].values[0]
    fig_emp = px.pie(values=[emp_agr , emp_ind , emp_ser] , names=['Agriculture' , 'Industry' , 'Services'])
    
    # Labour Force participation
    lab_mal = df1['Labour force participation (male)%'].values[0]
    lab_fem = df1['Labour force participation (female)%'].values[0]
    labour_force = [lab_mal, lab_fem]

    # Categories
    categories = ['Males', 'Females']

    # Define colors for males and females
    colors = ['royalblue', 'salmon']

    # Create a bar trace for males and females with different colors
    trace = go.Bar(x=categories, y=labour_force)

    # Create a figure and add the trace
    fig_lab = go.Figure(data=[trace])

    # Update layout
    fig_lab.update_layout(
        title='Comparison of participation in Labor force by Gender',
        xaxis_title='Gender',
        yaxis_title='Labour Force participation'
    )

    
    dict = {
        "Location":loc,
        "Population":pop,
        "GDP":gdp,
        "GDP_per_capita":gdp_pc,
        "Sex-Ratio":sr,
        "Urban Population":urb_pop,
        "Urban Population Growth":urb_gr,
        "Fertility Rate":fer_rat,
        "Infant Mortality Rate": imr
    }
    table = pd.DataFrame(dict , index=["Basic Information"]).swapaxes('index','columns')
    
    return loc,pop,gdp,gdp_pc,sr,urb_pop,urb_gr,fer_rat,imr,fig_econ,fig_trad,fig_emp,table,fig_lif,fig_lab

def age_class(df):
    x = df[[ 'country','Population_percent_(0-14)','Population_percent_(60+)']]
    df['Population_percent_(14-60)'] = 100.0 - (df['Population_percent_(0-14)'] + df['Population_percent_(60+)'])
    x = df[[ 'country','Population_percent_(0-14)','Population_percent_(14-60)','Population_percent_(60+)']]
    values = x[['Population_percent_(0-14)','Population_percent_(14-60)','Population_percent_(60+)']].values[0].tolist()
    fig = px.pie(names=['Youth Population(0-14)' , 'Working Population(14-60)' , 'Old Population(60+)'], values=values)
    return fig