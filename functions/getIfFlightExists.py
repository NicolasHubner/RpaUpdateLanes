def getIfTheFlightsExists(flight_data, flight_number, flight_AMS_date):
    
    for flight in flight_data:

        if str(flight['attributes']['flightDate']) == str(flight_AMS_date) and str(flight['attributes']['flightNumber']).zfill(4) == str(flight_number):
            return True, flight['id'], flight['attributes']['description']

    print("Flight not found:", flight_number , flight_AMS_date)
    return False