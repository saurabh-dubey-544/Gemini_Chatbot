import numpy as np


def overall_population(df):
    return df['Population (2017)'].sum()

def preprocess(df):
    df['Surface area (km2)'].iloc[25] = 328
    df['Surface area (km2)'].iloc[91] = 0.44
    df['Surface area (km2)'].iloc[130] = 374
    df['Surface area (km2)'].iloc[193] = 1886068
    
    df['Population (2017)'] = df['Population in thousands (2017)']*1000
    df.drop(columns = 'Population in thousands (2017)' , inplace=True)
    
    df['Sex ratio (m per 100 f, 2017)'].iloc[25] = 107.04
    df['Sex ratio (m per 100 f, 2017)'].iloc[169] = 99.96
    
    df['GDP: Gross domestic product (million current US$)'].iloc[3] = 600
    df['GDP: Gross domestic product (million current US$)'].iloc[25] = 650
    df['GDP: Gross domestic product (million current US$)'].iloc[41] = 9530
    df['GDP: Gross domestic product (million current US$)'].iloc[68] = 206
    df['GDP: Gross domestic product (million current US$)'].iloc[69] = 2980
    df['GDP: Gross domestic product (million current US$)'].iloc[73] = 4930
    df['GDP: Gross domestic product (million current US$)'].iloc[80] = 2344
    df['GDP: Gross domestic product (million current US$)'].iloc[84] = 9079
    df['GDP: Gross domestic product (million current US$)'].iloc[85] = 6001
    df['GDP: Gross domestic product (million current US$)'].iloc[91] = 16
    df['GDP: Gross domestic product (million current US$)'].iloc[100] = 6979
    df['GDP: Gross domestic product (million current US$)'].iloc[127] = 8900
    df['GDP: Gross domestic product (million current US$)'].iloc[130] = 2660
    df['GDP: Gross domestic product (million current US$)'].iloc[149] = 24938
    df['GDP: Gross domestic product (million current US$)'].iloc[150] = 1560
    df['GDP: Gross domestic product (million current US$)'].iloc[169] = 38
    df['GDP: Gross domestic product (million current US$)'].iloc[172] = 261
    df['GDP: Gross domestic product (million current US$)'].iloc[204] = 10
    df['GDP: Gross domestic product (million current US$)'].iloc[218] = 3790
    df['GDP: Gross domestic product (million current US$)'].iloc[224] = 188
    df['GDP: Gross domestic product (million current US$)'].iloc[225] = 908

    df['Region_combined'] = df['Region'].replace(['SouthernEurope','NorthernEurope','EasternEurope','WesternEurope'] , 'Europe')
    df['Region_combined'] = df['Region_combined'].replace(['WesternAsia','South-easternAsia','SouthernAsia','EasternAsia','CentralAsia'] , 'Asia')
    df['Region_combined'] = df['Region_combined'].replace(['EasternAfrica','WesternAfrica','MiddleAfrica','NorthernAfrica','SouthernAfrica'] , 'Africa')
    df['Region_combined'] = df['Region_combined'].replace(['Polynesia','Micronesia','Melanesia','Oceania'],'Oceania')
    
    median_gdp = df['GDP per capita (current US$)'][df['GDP per capita (current US$)'] != -99.0].median()
    df['GDP per capita (current US$)'] = df['GDP per capita (current US$)'].replace(-99.0 , median_gdp )
    
    df['Economy: Agriculture (% of GVA)'] = df['Economy: Agriculture (% of GVA)'].replace(-99.0 , 33.33)
    df['Economy: Industry (% of GVA)'] = df['Economy: Industry (% of GVA)'].replace(-99.0 , 33.33)
    df['Economy: Services and other activity (% of GVA)'] = df['Economy: Services and other activity (% of GVA)'].replace(-99.0 , 33.33)
    
    df['Overall Trade(million US$)'] = df['International trade: Exports (million US$)'] + df['International trade: Imports (million US$)']
    
    df['Overall Trade(million US$)'] = df['Overall Trade(million US$)'].replace([-198,0] , np.nan)
    
    df['Overall Trade percentage'] = (df['Overall Trade(million US$)']/df['Overall Trade(million US$)'].sum())*100
    
    df['Fertility rate, total (live births per woman)'] = df['Fertility rate, total (live births per woman)'].replace([0.0 , -99.0] , np.nan)
    
    df['Infant mortality rate (per 1000 live births'] = df['Infant mortality rate (per 1000 live births'].replace(-99.0 , np.nan )
    df['Infant mortality rate (per 1000 live births'].iloc[211] = 20.6
    df['Infant mortality rate (per 1000 live births'].iloc[224] = 4.07
    
    return df