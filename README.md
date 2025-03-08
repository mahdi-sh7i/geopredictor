# geopredictor
# Country Data Scraper and Predictor

This project scrapes country data from a sample website, processes the information, and uses machine learning to predict the area of a country based on its population. The data is also visualized using bar charts.

## Overview

The code performs the following steps:

1. **Data Scraping**: 
   - Utilizes the requests library to fetch HTML content from the website [scrapethissite.com](https://www.scrapethissite.com/pages/simple/).
   - Parses the HTML using BeautifulSoup to extract country names, capitals, populations, and areas.

2. **Data Enrichment**:
   - For each country, additional information such as region and subregion is retrieved using the countryinfo library.

3. **Database Storage** (optional):
   - The scraped and enriched data can be stored in a SQLite database for later use. This section is currently commented out but can be enabled if desired.

4. **Machine Learning Model**:
   - A Decision Tree Classifier from sklearn is trained using the population as input features to predict the area of countries.
   - Predictions are made for several countries based on their populations.

5. **Data Visualization**:
   - Two bar charts are generated using matplotlib:
     - Count of countries by region.
     - Count of countries by subregion.
   - Each bar in the charts is annotated with its respective count for clarity.

## Requirements

To run this code, ensure you have the following libraries installed:

