import pandas as pd
import plotly.express as px
from plotly.offline import plot
import os, re

os.chdir("E:\\類別資料分析")

titanic = pd.read_csv("E:\\類別資料分析\\titanic.csv", usecols=[1,2,3,4,5,6,7,8,9,10])

titanic['country'] = titanic['country'].fillna(value="Unknown")

titanic['class'] = titanic['class'].str.replace(r"\w+(.*)(crew|staff)$", "crew")

titanic_dropna_copy = titanic.copy()
titanic_dropna_copy = titanic_dropna_copy.dropna()
titanic_dropna_copy[titanic_dropna_copy['class'] == "3rd"].mean()
# class 3rd 的平均 age = 25.025760

titanic['age'] = titanic['age'].fillna(value=25.025760)

#titanic.to_csv("E:\\類別資料分析\\titanic1_ver1.csv")

country_name = pd.Series(titanic['country'].unique())
country_name = country_name.drop(16)
country_name.index = [i for i in range(48)]

iso_alpha3 = ["USA", "GBR", "NOR", "FRA", "LBN", "FIN", "SWE",
              "ARG", "CAN", "DNK", "IRL", "BGR", "CHE", "GBR",
              "BIH", "HUN", "IRL", "ITA", "IND", "GBR", "ZAF",
              "HRV", "GBR", "THA", "URY", "BEL", "POL", "AUS",
              "PER", "ESP", "EGY", "JPN", "SYR", "RUS", "SVN",
              "GRC", "TUR", "HKG", "AUT", "LVA", "YUG", "SVK",
              "DEU", "HRV", "CUB", "NLD", "MEX", "GUY"]

country_iso_dict = dict(zip(country_name, iso_alpha3))
ISO_alpha3 = titanic["country"].map(country_iso_dict)
titanic.insert(5, "ISO_alpha3", ISO_alpha3)

unknown_citizenship_num = sum(titanic['country'] == 'Unknown') #81人

titanic_map_plot_copy = titanic.copy()
titanic_map_plot_copy = titanic_map_plot_copy.drop(["embarked", "ticketno", "fare", "sibsp", "parch"], axis=1)
titanic_map_plot_copy['survived'] = titanic_map_plot_copy['survived'].replace(['no', 'yes'], [0, 1])

survival_rate = []
num_passenger = []
for country in iso_alpha3:
    r = titanic_map_plot_copy[titanic_map_plot_copy.ISO_alpha3 == country]
    survival_rate.append(r['survived'].sum()/r['survived'].count())
    num_passenger.append(r['survived'].count())

iso_SurvivalRate_dict = dict(zip(iso_alpha3, survival_rate))
titanic_map_plot_copy["SurvivalRate"] = titanic_map_plot_copy["ISO_alpha3"].map(iso_SurvivalRate_dict)
iso_NumPassenger_dict = dict(zip(iso_alpha3, num_passenger)) 
titanic_map_plot_copy["Num-of-Passenger"] = titanic_map_plot_copy["ISO_alpha3"].map(iso_NumPassenger_dict)


#畫圖
#------------------------------------------------------------------------------------------------------------
# Sun Burst Graph
fig = px.sunburst(data_frame=titanic, path=['class', 'gender', 'survived'],
                  color="age", color_continuous_scale=px.colors.sequential.PuRd, range_color=[0,75])

fig.update_traces(textinfo='label+percent entry')
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
plot(fig)
fig.write_html("D:\\類別資料分析\\titanic_sunburst.html")


# Choropleth Maps
choropleth_fig = px.choropleth(titanic_map_plot_copy, locations="ISO_alpha3",
                               color="SurvivalRate",
                               hover_data=["country", "Num-of-Passenger"],
                               projection='natural earth',
                               color_continuous_scale=px.colors.sequential.deep)

choropleth_fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
plot(choropleth_fig)
choropleth_fig.write_html("D:\\類別資料分析\\Survival-Rate-of-countries.html")
#---------------------------------------------------------------------------------------------------

#titanic_map_plot_group1 = titanic_map_plot_copy.set_index(['ISO_alpha3', 'class'])

