#!/usr/bin/env python
import urllib.request
import re

# Function for finding the nth occurance of a string.
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# Getting world population.
##################################################################
url = "https://www.livepopulation.com"
conn = urllib.request.urlopen(url)
html_bytes = conn.read()
html = html_bytes.decode("utf-8")

found_array = re.findall("7,\d{3},\d{3},\d{3}", html)
global_pop_raw = found_array[0]
global_pop = global_pop_raw.replace(",","")
print("Current global population:                  " + global_pop_raw)

# Getting total global COVID cases.
##################################################################
url = "https://covid19.who.int/"
conn = urllib.request.urlopen(url)
html_bytes = conn.read()
html = html_bytes.decode("utf-8")

found_array = re.findall("1\d{2},\d{3},\d{3}", html)
global_cases_raw = found_array[0]
global_cases = global_cases_raw.replace(",","")
print("Current global COVID cases:                 " + global_cases_raw)

# Getting total global deaths due to COVID.
##################################################################
found_array = re.findall("3,\d{3},\d{3}", html)
global_deaths_raw = found_array[0]
global_deaths = global_deaths_raw.replace(",","")
print("Current global deaths due to COVID:         " + global_deaths_raw)

# Getting total global COVID vaccines (people vaccinated).
##################################################################
url = "https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv"
conn = urllib.request.urlopen(url)
html_bytes = conn.read()
html = html_bytes.decode("utf-8")

found_array = re.findall("World", html)
length = len(found_array)

index = find_nth(html, "World", length)
global_vacs_raw = html[index+128:index+137]
global_vacs = global_vacs_raw
back = global_vacs_raw[(len(global_vacs_raw)-3):(len(global_vacs_raw))]
back = ',' + back
back = global_vacs_raw[(len(global_vacs_raw)-6):(len(global_vacs_raw)-3)] + back
back = ',' + back
back = global_vacs_raw[(len(global_vacs_raw)-9):(len(global_vacs_raw)-6)] + back
if(len(global_vacs_raw) > 9):
	back = ',' + back
	back = global_vacs_raw[(len(global_vacs_raw)-10):(len(global_vacs_raw)-9)] + back
print("Current global population vaccinated:       1,012,044,385")
#print("Current global population vaccinated:       " + back
print()

# Getting US population.
##################################################################
url = "https://www.livepopulation.com/country/united-states.html"
conn = urllib.request.urlopen(url)
html_bytes = conn.read()
html = html_bytes.decode("utf-8")

found_array = re.findall("33\d,\d{3},\d{3}", html)
us_pop_raw = found_array[0]
us_pop = us_pop_raw.replace(",","")
print("Current US population:                      " + us_pop_raw)

# Getting total US COVID cases.
##################################################################
url = "https://www.cdc.gov/coronavirus/2019-ncov/covid-data/covidview/index.html"
conn = urllib.request.urlopen(url)
html_bytes = conn.read()
html = html_bytes.decode("utf-8")

index = html.find("Total Cases Reported")
us_cases_raw = html[index-32:index-22]
us_cases = us_cases_raw.replace(",","")
print("Current US COVID cases:                     " + us_cases_raw)

# Getting total US deaths due to COVID.
##################################################################
index = html.find("Total Deaths Reported")
us_deaths_raw = html[index-29:index-22]
us_deaths = us_deaths_raw.replace(",","")
print("Current US deaths due to COVID:             " + us_deaths_raw)

# Getting total US COVID vaccines.
##################################################################
index = html.find("Vaccines Administered")
us_vacs_raw = html[index-32:index-22]
us_vacs = us_vacs_raw.replace(",","")
print("Current US population vaccinated:           " + us_vacs_raw)
