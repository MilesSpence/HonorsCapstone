#!/usr/bin/env python
import pandas as pd

# This file acquires the up to date data on COVID-19 and then computes the necessary probabilites
# for the model.

# Retrieving the data from Our World in Data's GitHub.
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
vac_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/United%20States.csv'
vac_data = pd.read_csv(url, usecols=['date','people_fully_vaccinated'])

my_filtered_csv = pd.read_csv(url, usecols=['iso_code','date','total_cases','new_cases','total_deaths','new_deaths'])

filtered = [[]]
y = 0
US_pop =[]

for x in range(len(my_filtered_csv)):
    if (my_filtered_csv['iso_code'][x] == "USA"):
        filtered.insert(y, [my_filtered_csv['date'][x], my_filtered_csv['total_cases'][x], my_filtered_csv['new_cases'][x], 0, my_filtered_csv['total_deaths'][x], my_filtered_csv['new_deaths'][x], 0, vac_data['people_fully_vaccinated'][x]])
        y += 1

# Calculating the probabilities
US_pop = 330122733
all_infection_rates = []

for z in range(390, len(filtered)-3):
        all_infection_rates.append((int(filtered[z][1]))/(US_pop-int(filtered[z+1][7])))

avg_infect_rate = 0
avg_sum = 0.0

for p in range(len(all_infection_rates)):
    avg_sum += float(all_infection_rates[p])

avg_infect_rate = avg_sum/len(all_infection_rates)

print("Average infection probability:   " + str(avg_infect_rate*100))

all_mortality_rates = []

for z in range(390, len(filtered)-3):
        all_mortality_rates.append(int(filtered[z][4])/int(filtered[z][1]))

avg_mort_rate = 0
avg_sum = 0.0

for q in range(len(all_mortality_rates)):
    avg_sum += float(all_mortality_rates[q])

avg_mort_rate = avg_sum/len(all_mortality_rates)

print("Average mortality probability:    " + str(avg_mort_rate*100))

all_vac_rates = []

for z in range(391, len(filtered)-3):
        all_vac_rates.append((int(filtered[z+1][7])-int(filtered[z][7]))/US_pop)

avg_vac_rate = 0
avg_sum = 0.0

for q in range(len(all_vac_rates)):
    avg_sum += float(all_vac_rates[q])

avg_vac_rate = avg_sum/len(all_vac_rates)

print("Average vaccination probability:  " + str(avg_vac_rate*100))

total_cases = filtered[len(filtered)-2][1]
