"""
Proyecto Shin DMS
@author: Jose Pablo Castro
@author: David Jimenez
"""
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
data = pd.read_csv('record.csv')

# Assuming your CSV file has columns 'time' and 'score', you can change these to match your actual column names
time_column = 'time'
score_column = 'score'

# Extract the time and score data from the DataFrame
time = data[time_column]
score = data[score_column]

# Create a time vs. score plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.plot(time, score)
plt.title('Learning Curve in AI')
plt.xlabel('Time')
plt.ylabel('Score')
plt.grid(True)
plt.show()