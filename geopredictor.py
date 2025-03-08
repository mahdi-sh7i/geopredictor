import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn import tree
import sqlite3
from countryinfo import CountryInfo
import matplotlib.pyplot as plt

# Fetch the HTML content of the webpage
res = requests.get('https://www.scrapethissite.com/pages/simple/')
soup = BeautifulSoup(res.text, 'html.parser')

# Connect to SQLite database
conn = sqlite3.connect('/home/mahdi/all_pro/geopredictor/data.db')
cur = conn.cursor()

# Extract country names and related data from the HTML
countries = soup.find_all('h3')
other = soup.find_all('span')

# Initialize lists to hold country data
list_capital = []
list_population = []
list_area = []
list_countries = []
list_region = []
list_subregion = []

# Loop through each country and extract relevant information
for i in range(0, len(countries)):
    list_countries.append(countries[i].text.strip())  
    list_capital.append(other[i * 3].text.strip())
    list_population.append(other[i * 3 + 1].text.strip())
    list_area.append(other[i * 3 + 2].text.strip())

# Retrieve additional information (region and subregion) for each country
for country in list_countries:
    info = CountryInfo(country)
    try:
        list_region.append(info.region())
        list_subregion.append(info.subregion())
    except:
        # If information is not found, append 'None'
        list_region.append('None')
        list_subregion.append('None')

# Uncomment the following block to save data into the database
'''
# Zip the lists together into a single iterable object
zipped = zip(list_countries, list_capital, list_population,
              list_area, list_region, list_subregion)
result = list(tuple(zipped))

# Create a table in the database if it doesn't already exist
q = """
CREATE TABLE IF NOT EXISTS Countries (Countrie text,
                                      Capital text,
                                      Population integer,
                                      Area integer,
                                       Region text,
                                       Subregion text)
"""
cur.execute(q)

# Insert the data into the database
q1 = "INSERT INTO Countries VALUES (?, ?, ?, ?, ?, ?)"
cur.executemany(q1, result)

# Fetch all records from the Countries table (this line is incomplete)
cur.execute("select * from Countries").fetchall()
conn.commit()
conn.close()
'''

# Create a DataFrame from the collected data
data = {'Countries': list_countries,
        'Capital': list_capital,
        'Population': list_population,
        'Area(km^2)': list_area,
        'Region': list_region,
        'Subregion': list_subregion}
df = pd.DataFrame(data)

# Print the DataFrame to view the collected data
print(df)

# Prepare data for machine learning (ML)
x = pd.DataFrame(data, columns=['Population'])
y = pd.DataFrame(data, columns=['Area(km^2)'])

# Train a Decision Tree Classifier on the data
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

# New data points for prediction
new_data = [[85000], [5000000], [30000000], [80000], [14000], [300000]]
p = clf.predict(new_data)

# Print predictions for specific countries based on input populations
print('Andorra Area(km^2):468.0 and Population:84000 and input ml 85000 and Out for Area is:', p[0])
print('United Arab Emirates Area(km^2):82880.0 and Population:4975593 and input ml 5000000 and Out for Area is:', p[1])
print('Afghanistan Area(km^2):647500.0 and Population:29121286 and input ml 30000000 and Out for Area is:', p[2])
print('Antigua and Barbuda Area (km^2):443.0 and Population:86754 and input ml 80000 and Out for Area is:', p[3])
print('Anguilla Area(km^2):102.0 and Population:13254 and input ml 14000  and Out for Area is:', p[4])
print('Albania Area(km^2):28748.0 and Population:2986952 and input ml 300000 and Out for Area is:', p[5])

# Plotting the count of countries by region
a1 = df["Region"].value_counts().plot(kind="bar", figsize=[12, 4])
plt.xticks(rotation=75, horizontalalignment="center", fontsize=10)
plt.xlabel("Region", fontsize=15)
plt.ylabel("Count", fontsize=15)
plt.yticks(fontsize=15)
plt.title("Region", fontsize=20)

# Annotate bars with their heights
for p in a1.patches:
    a1.annotate(str(p.get_height()), xy=(p.get_x() + 0.2, p.get_height() + 0.1), fontsize=15)
plt.show()

# Plotting the count of countries by subregion
a2 = df["Subregion"].value_counts().plot(kind="bar", figsize=[12, 4])
plt.xticks(rotation=75, horizontalalignment="center", fontsize=10)
plt.xlabel("Subregion", fontsize=15)
plt.ylabel("Count", fontsize=15)
plt.yticks(fontsize=15)
plt.title("Subregion", fontsize=20)

# Annotate bars with their heights for subregions
for p1 in a2.patches:
    a2.annotate(str(p1.get_height()), xy=(p1.get_x() + 0.2, p1.get_height() + 0.1), fontsize=15)
plt.show()
