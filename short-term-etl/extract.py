"""Script with functions that extract the plant data from the API."""

from asyncio import run, gather
from aiohttp import ClientSession


async def get_plant_data(session, url: str) -> dict | None:
    """Fetches the plant data from the API with the url provided."""

    searching = True

    # Keep pinging the API until the raspberry pi works
    while searching:
        response = await session.request('GET', url=url)
        if response.status != 500:
            searching = False

    if response.status == 200:
        content = await response.json()
        return content

    # No plant found, so return None
    return None


async def get_batch_plant_data(start_id: int, end_id: int) -> list[dict]:
    """Gets a batch of plant data between the provided plant ids."""

    urls = [f"https://sigma-labs-bot.herokuapp.com/api/plants/{i}"
            for i in range(start_id, end_id)]

    async with ClientSession() as session:
        tasks = [get_plant_data(session, url) for url in urls]
        responses = await gather(*tasks)

    return responses


def extract_all_plant_data(batch_size: int = 10) -> list[list]:
    """
    Extracts all of the plant data with a chosen batch size.
    The process will stop if a batch contains no plant data.
    """

    plants_exist = True
    i = 0
    plant_data = []

    while plants_exist:
        start = batch_size*i + 1
        end = batch_size*(i+1) + 1

        plants = run(get_batch_plant_data(start, end))

        if not any(plants):
            plants_exist = False
        else:
            plant_data.extend(plants)
            i += 1

    return [p for p in plant_data if p]
