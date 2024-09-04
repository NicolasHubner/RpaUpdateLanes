from datetime import datetime, timedelta
import random
import re
from bs4 import BeautifulSoup

import requests
from functions.getAllFlights import getAllFlights
from functions.getIfFlightExists import getIfTheFlightsExists
from functions.loginUser import login_user
from functions.updateFlights import UpdateFlightsAirlineLatam

from functions.constants import arrayIcaoIata, arrayIcaoIataLatam

username = "*****"
password = "*****"
response = login_user(username, password)

token = response["data"]["login"]["jwt"]

if response:
    print("JWT Token:", response["data"]["login"]["jwt"])
    user_data = response["data"]["login"]["user"]
    print("User ID:", user_data["id"])
    print("Username:", user_data["username"])
    print("Email:", user_data["email"])

all_flights = getAllFlights(token)

# def updateAirlineLatamFlights():
#     if all_flights:
#             all_flights_dict = all_flights['data']['flights']['data']
            
#             for flight in all_flights_dict:

#                 if 'JJ' in flight['attributes']['description'] or 'LTM' in flight['attributes']['description']:
#                     UpdateFlightsAirlineLatam(token, flight['id'], flight['attributes']['gate'], flight['attributes']['BOX'], flight['attributes']['prefix'], flight['attributes']['aircraft_model'])
                    
timeNow = datetime.now().strftime("%H:%M:%S")

timeEnd = datetime.now().strftime("%H:%M:%S")

timeToRun = datetime.strptime(timeEnd, '%H:%M:%S') - datetime.strptime(timeNow, '%H:%M:%S')

print("Time to run:", timeToRun)


# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # Add more user agents as needed
]

headers = {'User-Agent': random.choice(user_agents)}


payload = {
    'type': 'A',
    'username': '',
    'pwd': '',
    'Captcha': ''
}

def url (type):
  return f"https://ams.gru.com.br/{type}.html"

newArrayOnlyIcao = []

for index, row in enumerate(arrayIcaoIataLatam):
    if row['ICAO'] not in newArrayOnlyIcao:
        newArrayOnlyIcao.append(row['ICAO'])

def updateAirlineLatamFlightsArrival():
  today = datetime.now().strftime("%d/%m/%Y")

  today_more_one_day = datetime.now() + timedelta(days=1)
  today_more_one_day = today_more_one_day.strftime("%d/%m/%Y")

  type = "arrival" # or "arrival

  timeout_seconds = 30

  response = requests.post("https://ams.gru.com.br/arrival.html", data=payload, headers=headers, timeout=timeout_seconds)


  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      print("Page Title:", soup.title.text)


  # tbody = soup.find('tbody')

      if all_flights:
        all_flights_dict = all_flights['data']['flights']['data']
      
      for index,row in enumerate(soup.find_all('tr')):
          # Extract data from each cell in the row
          cells = row.find_all(['td', 'th'])

          if len(cells) == 1:
              date_string = cells[0].text.strip()
              date_match = re.search(r'\d{2}/\d{2}/\d{4}', date_string)

              if date_match:
                  extracted_date = date_match.group()
                  print("Extracted Date:", extracted_date)

                  # Convert extracted_date to datetime object for comparison
                  extracted_date_datetime = datetime.strptime(extracted_date, "%d/%m/%Y")
                  print("More one Day", today_more_one_day)
                  if extracted_date == today_more_one_day:
                      print('Date is one day ahead of today:', today)
                      today = extracted_date_datetime.strftime("%d/%m/%Y")
                  else:
                      print('Date is not one day ahead of today.')
              else:
                  print("Date not found in the string.")

          if len(cells) >= 12 and cells[2].find('div') and cells[2].find('div').text.strip() in newArrayOnlyIcao:

                      # dateFlight=today
                      # time = cells[0].text.strip() if cells[0].text.strip() else '-'
                      flight_number = cells[3].text.strip()
                      # gate = cells[6].text.strip()
                      box = cells[7].text.strip()
                      prefix = cells[8].text.strip()
                      aircraft_model = cells[9].text.strip()
                      # estimated_time = cells[10].text.strip()
                      
                      flightDateFormated = datetime.strptime(today, '%d/%m/%Y')
                      
                      flightDateFormated = flightDateFormated.strftime('%Y-%m-%d')
                      
                      isFlightExists = getIfTheFlightsExists(all_flights_dict, str(flight_number), flightDateFormated)

                      if isFlightExists:
                          gate = None
                          # print("isFlightExists", isFlightExists[1], box, prefix, aircraft_model)
                          # print("\n")
                          if 'JJ' in isFlightExists[2] or 'LA' in isFlightExists[2] or 'LTM' in isFlightExists[2]:

                            UpdateFlightsAirlineLatam(
                                  token,
                                  isFlightExists[1],
                                  gate,
                                  box,
                            )


def updateAirlineLatamFlightsDeparture():
  today = datetime.now().strftime("%d/%m/%Y")

  today_more_one_day = datetime.now() + timedelta(days=1)
  today_more_one_day = today_more_one_day.strftime("%d/%m/%Y")

  type = "departure" # or "arrival

  timeout_seconds = 30

  response = requests.post("https://ams.gru.com.br/departure.html", data=payload, headers=headers, timeout=timeout_seconds)


  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      print("Page Title:", soup.title.text)


  # tbody = soup.find('tbody')

      if all_flights:
        all_flights_dict = all_flights['data']['flights']['data']
      
      for index,row in enumerate(soup.find_all('tr')):
          # Extract data from each cell in the row
          cells = row.find_all(['td', 'th'])

          if len(cells) == 1:
              date_string = cells[0].text.strip()
              date_match = re.search(r'\d{2}/\d{2}/\d{4}', date_string)

              if date_match:
                  extracted_date = date_match.group()
                  print("Extracted Date:", extracted_date)

                  # Convert extracted_date to datetime object for comparison
                  extracted_date_datetime = datetime.strptime(extracted_date, "%d/%m/%Y")
                  print("More one Day", today_more_one_day)
                  if extracted_date == today_more_one_day:
                      print('Date is one day ahead of today:', today)
                      today = extracted_date_datetime.strftime("%d/%m/%Y")
                  else:
                      print('Date is not one day ahead of today.')
              else:
                  print("Date not found in the string.")

          if len(cells) >= 12 and cells[2].find('div') and cells[2].find('div').text.strip() in newArrayOnlyIcao:

                      flight_number = cells[3].text.strip()
                      gate = cells[7].text.strip()
                      box = cells[8].text.strip()

                      flightDateFormated = datetime.strptime(today, '%d/%m/%Y')
                      
                      flightDateFormated = flightDateFormated.strftime('%Y-%m-%d')
                      
                      isFlightExists = getIfTheFlightsExists(all_flights_dict, str(flight_number), flightDateFormated)

                      if isFlightExists:
                          if 'JJ' in isFlightExists[2] or 'LA' in isFlightExists[2] or 'LTM' in isFlightExists[2]:
                            
                            UpdateFlightsAirlineLatam(
                                  token,
                                  isFlightExists[1],
                                  gate,
                                  box,
                            )


now = datetime.now()

# updateAirlineLatamFlightsArrival()

print("End update flights arrival")

updateAirlineLatamFlightsDeparture()

print("End update flights departure")

end = datetime.now()

timeToRun = end - now

print("Time to run:", timeToRun)

print("End update flights")
