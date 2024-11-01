import csv
import os

current_directory = os.getcwd()
entries = os.listdir(current_directory)
print(entries)

filename = "metingen_0.csv"
counter = 0
while filename in entries:
    filename = f"metingen_{counter}.csv"
    counter += 1

with open(f"{filename}", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["I", "U"])
