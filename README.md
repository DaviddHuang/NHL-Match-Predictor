# NHL Match Predictor

## Overview
This project is designed to predict the outcomes of NHL (National Hockey League) matches using machine learning. It combines historical match data with statistical features derived from game logs to train a model capable of making predictions for future matches. Additionally, the project includes a web scraping module to gather the latest game logs from Hockey Reference.

## Project Structure
The project consists of two main components:

1. **Web Scraping (Data Collection)**
2. **NHL Match Predictor (Machine Learning Model)**

### 1. Web Scraping
This module scrapes the latest NHL game logs from Hockey Reference. It retrieves data for all NHL teams for the 2024 season and stores it in a CSV file. Key steps include:

- **Scraping Team Links:** Extracts URLs for each team's game logs.
- **Extracting Game Data:** Parses the game data and stores it in a pandas DataFrame.
- **Saving to CSV:** The combined game data is saved to `matches.csv`.

### 2. NHL Match Predictor
This component uses historical match data to predict match outcomes using a Random Forest Classifier. Key steps in the process include:

- **Feature Engineering:** Rolling averages of team statistics (such as Goals For, Goals Against, Shots, Penalties, etc.) are calculated over the last three games to create predictive features.
- **Model Training:** The data is split into a training set (before January 25, 2024) and a test set (on or after January 25, 2024). A Random Forest model is trained on the training data and then evaluated on the test set.
- **Performance Metrics:** The precision score is calculated to evaluate the model's performance.
