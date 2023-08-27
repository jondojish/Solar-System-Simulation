import requests, json, datetime


def get_data(planet, date):
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    # Define the time span:
    start_time = date.strftime("%Y-%m-%d")
    stop_time = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # Build the appropriate URL for this API request:
    # IMPORTANT: You must encode the "=" as "%3D" and the ";" as "%3B" in the
    #            Horizons COMMAND parameter specification.
    horizons_id = ""
    if planet == "earth":
        horizons_id = "399"
        lines = [58, 59]
    elif planet == "mercury":
        horizons_id = "199"
        lines = [51, 52]
    elif planet == "venus":
        horizons_id = "299"
        lines = [51, 52]
    elif planet == "mars":
        horizons_id = "499"
        lines = [53, 54]
    elif planet == "jupiter":
        horizons_id = "599"
        lines = [52, 53]
    elif planet == "saturn":
        horizons_id = "699"
        lines = [52, 53]
    elif planet == "uranus":
        horizons_id = "799"
        lines = [52, 53]
    elif planet == "neptune":
        horizons_id = "899"
        lines = [52, 53]

    if planet == "moon":
        horizons_id = "301"
        lines = [54, 55]
        url += (
            "?format=json&EPHEM_TYPE=VECTORS&OBJ_DATA=YES&MAKE_EPHEM=YES&CENTER='500'"
        )
        url += f"&COMMAND='{horizons_id}'%3B'&START_TIME='{start_time}'&STOP_TIME='{stop_time}'"
    else:
        url += (
            "?format=json&EPHEM_TYPE=VECTORS&OBJ_DATA=YES&MAKE_EPHEM=YES&CENTER='@10'"
        )
        url += f"&COMMAND='{horizons_id}'%3B'&START_TIME='{start_time}'&STOP_TIME='{stop_time}'"
    # Submit the API request and decode the JSON-response:
    response = requests.get(url)
    try:
        data = response.text
        with open("info.json", "w") as f:
            pos_data = []
            vel_data = []
            pos_data = json.loads(data)["result"].split("\n")[lines[0]]
            vel_data = json.loads(data)["result"].split("\n")[lines[1]]
            print("ddd", pos_data, vel_data)
            pos_data = list(map(lambda x: x.strip("=VXYZ"), pos_data.split(" ")))
            vel_data = list(map(lambda x: x.strip("=VXYZ"), vel_data.split(" ")))
            print(pos_data, vel_data)
            pos = []
            vel = []
            for i in pos_data:
                if i != "":
                    pos.append(float(i) * 10**3)
            for i in vel_data:
                if i != "":
                    vel.append(float(i) * 10**3)
        return {"pos": pos, "vel": vel}
    except ValueError:
        print("Unable to decode JSON results")


# get_data("earth")
