"""Script with functions that extract the plant data from the API."""

from requests import get


def request_plant(plant_id: int) -> dict:
    """Request plant information from the API for a given plant id."""

    return get(f"https://sigma-labs-bot.herokuapp.com/api/plants/{plant_id}")


def extract_all_plant_data() -> list[dict]:
    """
    Extract all plant data from the API, 
    stopping after 10 consecutive missing plants.
    """

    searching = True
    i = 1
    count = 0
    plants = []

    while searching:
        plant_req = request_plant(i)

        if plant_req.status_code == 404:
            i += 1
            count += 1
            if count == 10:
                searching = False
        else:
            count = 0
            while plant_req.status_code == 500:
                plant_req = request_plant(i)

            plants.append(plant_req.json())
            i += 1

    return plants


if __name__ == "__main__":
    data = extract_all_plant_data()
    print(data)
