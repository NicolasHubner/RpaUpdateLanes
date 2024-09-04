import requests

from functions.constants import ENUM_TYPE_AIRCRAFT
from constants import url

def UpdateFlightsAirlineLatam(token, id, gate, box):
    
    # bodyType = next((item for item in ENUM_TYPE_AIRCRAFT if item['NAME'] == aircraft_model), None).get('BODY')
    
    objectToCreate = {
        "id": id,
        "gate": gate,
        "box": box,
    }
    
    query = """
        mutation UpdateFlightDetails(
            $id: ID!
            $airline: ID
            $gate: String
            $box: String
            ) {
            updateFlight(
                id: $id
                data: {
                    airline: $airline
                    gate: $gate
                    BOX: $box
                }
            ) {
                data {
                id
                attributes {
                    description
                    BOX
                    gate
                }
                }
            }
            }
        """
    
    variables = {
            "id": objectToCreate['id'],
            "airline": 1,
            "box": objectToCreate['box'],
            "gate": objectToCreate['gate'],
        }
    
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        json_response = response.json()
        print("Flight updated successfully:", json_response)
    else:
        print("Request failed:", response.status_code, response.text)
        return None