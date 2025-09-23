"""Script to clean and validate the plants data."""
from datetime import datetime

def clean_plant_id(data) -> int:
    """Clean plant id."""
    if not isinstance(data["plant_id"], int):
        raise ValueError("Invalid plant id type")
    
    if data["plant_id"] <= 0:
        raise ValueError("Invalid plant id")
    
    return data["plant_id"]


def clean_plant_name(data) -> str:
    """Clean plant name."""
    if not isinstance(data["name"], str):
        raise ValueError("Invalid name type")

    return data["name"].strip()
    
def clean_temperature(data) -> float:
    """Clean temperature."""
    if not isinstance(data["temperature"], float):
        raise ValueError("Invalid temperature type")
    
    if not (-10 <= data["temperature"] <= 60):
        raise ValueError("Invalid temperature value")
    
    return data["temperature"]


def clean_origin_location(data) -> dict:
    """Clean origin location."""
    if not isinstance(data["origin_location"]["city"], str):
        raise ValueError("Invalid city value")
    
    if not isinstance(data["origin_location"]["country"], str):
        raise ValueError("Invalid country value")
    
    data["origin_location"]["city"] = data["origin_location"]["city"].strip().title()

    data["origin_location"]["country"] = data["origin_location"]["country"].strip().title()

    return {
        "city": data["origin_location"]["city"],
        "country": data["origin_location"]["country"],
    }

def clean_botanist(data) -> dict:
    """Clean botanist."""
    if not isinstance(data["botanist"]["name"], str):
        raise ValueError("Invalid botanist name value")

    if not isinstance(data["botanist"]["email"], str):
        raise ValueError("Invalid botanist email value")

    data["botanist"]["name"] = data["botanist"]["name"].strip().title()

    data["botanist"]["email"] = data["botanist"]["email"].strip().lower()

    return {
        "name": data["botanist"]["name"],
        "email": data["botanist"]["email"]
    }


def clean_last_watered(data) -> datetime:
    """Clean last watered."""
    if not isinstance(data["last_watered"], str):
        raise ValueError("Invalid last watered value")
    
    data["last_watered"] = datetime.fromisoformat(data["last_watered"])

    return data["last_watered"]

def clean_soil_moisture(data) -> float:
    """Clean soil moisture."""
    if not isinstance(data["soil_moisture"], float):
        raise ValueError("Invalid soil moisture value")
    
    if not (0 <= data["soil_moisture"] <= 100):
        raise ValueError("Invalid soil moisture value")
    
    return data["soil_moisture"]

def clean_recording_taken(data) -> datetime:
    """Clean recording taken."""
    if not isinstance(data["recording_taken"], str):
        raise ValueError("Invalid recording taken value")

    data["recording_taken"] = datetime.fromisoformat(data["recording_taken"])

    return data["recording_taken"]

def clean_plants(data) -> dict:
    """Clean all plant data."""
    cleaned_data = {
        "plant_id": clean_plant_id(data),
        "name": clean_plant_name(data),
        "temperature": clean_temperature(data),
        "origin_location": clean_origin_location(data),
        "botanist": clean_botanist(data),
        "last_watered": clean_last_watered(data),
        "soil_moisture": clean_soil_moisture(data),
        "recording_taken": clean_recording_taken(data)
    }

    return cleaned_data

if __name__ == "__main__":
    data = {
        "plant_id": 8,
        "name": "Bird of paradise",
        "temperature": 16.3483444707664,
        "origin_location": {
            "latitude": 54.1635,
            "longitude": 8.6662,
            "city": "Edwardfurt",
            "country": "Liberia"
        },
        "botanist": {
            "name": "Bradford Mitchell DVM",
            "email": "bradford.mitchell.dvm@lnhm.co.uk",
            "phone": "(230) 859-2277 x3537"
        },
        "last_watered": "2025-09-22T13:33:20.000Z",
        "soil_moisture": 31.7511122641509,
        "recording_taken": "2025-09-23T09:39:03.821Z",
        "scientific_name": [
            "Heliconia schiedeana 'Fire and Ice'"
        ]
    }
