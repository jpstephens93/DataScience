from utils.functions import coordinates_range
import pandas as pd
import requests


def starbucks_drive_thru(range_diff):

    latitude = coordinates_range(50, 60, range_diff)
    longitude = coordinates_range(-8, 2, range_diff)

    base_api_url = 'https://www.starbucks.co.uk/api/v1/store-finder?&place=United+Kingdom'

    stores = []
    for i in latitude:
        # i = latitude[0]
        for j in longitude:
            # j = longitude[0]
            url = base_api_url + f'&latLng={str(i)}%2C{str(j)}'
            page = requests.get(url)

            for store in page.json()['stores']:
                drive_thru = 0
                for amenity in store['amenities']:
                    if amenity['description'] == 'Drive-Through':
                        drive_thru = 1
                stores.append([store['name'], store['address'], drive_thru, store['coordinates']])

            if not str(page) == '<Response [200]>':
                print(f'ERROR: Coordinates ({i}, {j}) not found')
            else:
                print(f'Coordinates ({i}, {j}) success')

    df = pd.DataFrame(stores, columns=['StoreName', 'Address', 'DriveThru', 'Coordinates'])
    df_unique = df.drop_duplicates('Address')

    bps = str(int(range_diff * 100))

    df_unique.to_excel(f'Starbucks/data/Stores_{bps}bp_Range.xlsx', index=False)


if __name__ == '__main__':
    starbucks_drive_thru(range_diff=0.1)
