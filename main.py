import math
import requests
import json
import csv
import operator
import argparse
import matplotlib.pyplot as plt
import folium

response_API = requests.get(
    'https://data.cityofnewyork.us/resource/au7q-njtk.json')
data = response_API.text
json_data = json.loads(data)


def sum_racks_by_borough(borough_name, json_data):
    total_bike_racks = 0
    for item in json_data:
        if borough_name == item["boro_name"]:
            total_bike_racks += 1
    return total_bike_racks


def get_racks_by_borough():
    # 1. Which boroughs have the most bike racks from greatest to least? Please include the count of bikes for each borough.
    print("Number of bike racks in Brooklyn:",
          sum_racks_by_borough('Brooklyn', json_data))
    print("Number of bike racks in Manhattan:",
          sum_racks_by_borough('Manhattan', json_data))
    print("Number of bike racks in Queens:",
          sum_racks_by_borough('Queens', json_data))
    print("Number of bike racks in the Bronx:",
          sum_racks_by_borough('Bronx', json_data))
    print("Number of bike racks in Staten Island",
          sum_racks_by_borough('Staten Island', json_data))


def sum_racks_by_subtype(asset_subtype, json_data):
    total_bike_racks = 0
    for item in json_data:
        if asset_subtype == item["assetsubty"]:
            total_bike_racks += 1
    return total_bike_racks


def get_rack_subtype_totals():
    # 2. How many of each subtype of bike rack are there for entire city? The subtype is denoted by the “assetsubty” field in the api data.
    print("Number of Small Hoop bike racks:",
          sum_racks_by_subtype("Small Hoop", json_data))
    print("Number of Large Hoop bike racks:",
          sum_racks_by_subtype("Large Hoop", json_data))
    print("Number of U-Rack bike racks:",
          sum_racks_by_subtype("U-Rack", json_data))
    print("Number of Wave Rack bike racks:",
          sum_racks_by_subtype("Wave Rack", json_data))


def make_json(csvFilePath, jsonFilePath):
    data = {}
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['ntaname']
            data[key] = rows['shape_area']
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def map_nta_names(json_data):
    for item in json_data:
        if item['ntaname'] == 'Greenwich Village':
            item['ntaname'] = 'West Village'
        elif item['ntaname'] == 'Sunset Park (West)':
            item['ntaname'] = 'Sunset Park West'
        elif item['ntaname'] == 'Sunset Park (East)':
            item['ntaname'] = 'Sunset Park East'
        elif item['ntaname'] == 'Chelsea-Hudson Yards':
            item['ntaname'] = 'Hudson Yards-Chelsea-Flatiron-Union Square'
        elif item['ntaname'] == 'Midtown South-Flatiron-Union Square':
            item['ntaname'] = 'Hudson Yards-Chelsea-Flatiron-Union Square'
        elif item['ntaname'] == 'Crown Heights (North)':
            item['ntaname'] = 'Crown Heights North'
        elif item['ntaname'] == 'Crown Heights (South)':
            item['ntaname'] = 'Crown Heights South'
    return json_data


def convert_square_feet_to_miles(ntaData):
    for key in ntaData:
        ntaData[key] = float(ntaData[key]) * float(0.00000003587006428)
    return ntaData


def sum_racks_by_nta(json_data):
    count = {}
    for item in json_data:
        if not item['ntaname'] in count:
            count[item['ntaname']] = 1
        else:
            count[item['ntaname']] += 1
    return count


def get_top_five_ntas():
    # 3. What are the top five NTAs based on bike racks per square mile? Please include the count of bike racks per square mile for each of the five.
    csvFilePath = r'NTATable.csv'
    jsonFilePath = r'NTATable.json'
    make_json(csvFilePath, jsonFilePath)
    f = open('NTATable.json')
    ntaData = convert_square_feet_to_miles(json.load(f))
    fixed_data = map_nta_names(json_data)
    count = {}
    # Get count of bike racks in each NTA and sort by rack count
    for item in fixed_data:
        if not item['ntaname'] in count:
            count[item['ntaname']] = 1
        else:
            count[item['ntaname']] += 1
    rack_counts_descending = dict(
        sorted(count.items(), key=operator.itemgetter(1), reverse=True)[:10])
    newCount = {}
    # Calculate bike racks per square mile
    for item in rack_counts_descending:
        for key in ntaData:
            if item == key:
                newCount[item] = math.floor(
                    rack_counts_descending[item] // ntaData[key])
    top_five_rack_counts_by_square_mile = dict(
        sorted(newCount.items(), key=operator.itemgetter(1), reverse=True)[:5])
    print(top_five_rack_counts_by_square_mile)


def get_dates(json_data):
    bikes_installed = {}
    for item in json_data:
        if item.get("date_inst") is not None:
            if not item["date_inst"][0:4] in bikes_installed:
                bikes_installed[item["date_inst"][0:4]] = 1
            else:
                bikes_installed[item["date_inst"][0:4]] += 1
        else:
            item["date_inst"] = "no date"
            if not item["date_inst"] in bikes_installed:
                bikes_installed[item["date_inst"]] = 1
            else:
                bikes_installed[item["date_inst"]] += 1
    return bikes_installed


def sum_racks_by_year(year, json_data):
    total_bike_racks = 0
    for item in json_data:
        if year == item["date_inst"][0:4]:
            total_bike_racks += 1
    return total_bike_racks


def make_rack_total_graph():
    # 4. How has the total bike racks installed changed over time? Please create a graph of the cumulative count of installed bike racks per time interval of your choice to answer this question.
    bikes_installed = get_dates(json_data)
    sorted_bikes = dict(sorted(bikes_installed.items()))
    items = sorted_bikes.items()
    years = []
    total_bikes_per_year = []
    for index, item in enumerate(items):
        years.append(item[0])
        if len(total_bikes_per_year) == 0:
            total_bikes_per_year.append(item[1])
        else:
            previousIndex = (index + len(items) - 1) % len(items)
            total_bikes_per_year.append(
                total_bikes_per_year[previousIndex] + item[1])

    plt.plot(years, total_bikes_per_year)
    plt.xlabel('years')
    plt.ylabel('number of bike racks')
    plt.title('Number of bike racks built over time')
    plt.show()


def create_rack_marker_map():
    # Optional bonus task: Using a geospatial data package of your choice, map of all of the data in any meaningful way of your choice and display a graphic of the map.
    # Please provide a brief explanation of your graphic.
    map = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

    tooltip = "Click me!"

    for item in json_data:
        folium.Marker([item["the_geom"]["coordinates"][1], item["the_geom"]["coordinates"][0]],
                      popup=folium.Popup(item["ifoaddress"] + ", " + item["ntaname"], min_width=300, max_width=300), tooltip=tooltip).add_to(map)

    map.save("my_map.html")

    print("done")


def main():
    parser = argparse.ArgumentParser(
        description="Choose which question to run by typing 'python main.py' followed by the question number into the terminal.")
    parser.add_argument('question', type=int,
                        help="Choose a question number between 1 and 5")
    args = parser.parse_args()
    if args.question == 1:
        get_racks_by_borough()
    elif args.question == 2:
        get_rack_subtype_totals()
    elif args.question == 3:
        get_top_five_ntas()
    elif args.question == 4:
        make_rack_total_graph()
    elif args.question == 5:
        create_rack_marker_map()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
