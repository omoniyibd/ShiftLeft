import requests
import time
import pandas as pd


def get_data():

    # Get data from source using provided API

    with open('ShiftLeft.txt') as file:  # Load authentication keys
        sl_auth = file.readlines()
        token = sl_auth[1].replace('\n', '')
        orgID = sl_auth[0].replace('\n', '')
        appID = sl_auth[2].replace('\n', '')

    # Inserting variables into the uri
    urls = [f'https://www.shiftleft.io/api/v4/orgs/{orgID}/apps/{appID}/findings']
    headers = {"Authorization": f'Bearer {token}'}
    counter = 1
    data_list = []

    # Exract data from uri and append it to the list
    for link in urls:
        print('Fetching over 4000 requests from API, please wait')
        response = requests.get(link, headers=headers).json()
        findings = response['response']['findings']

        for finding in findings:
            data = {}
            for tag in finding['tags']:
                data[tag['key']] = tag['value']
            data_list.append(data)
        print('Current page completed:')

        # If there is next_page then append the next_page link to list of urls
        if 'next_page' in response:
            urls.append(response['next_page'])
            counter += 1
            print('Working on next page: \n')
        else:
            print('Final request.')
        time.sleep(2)

    return data_list


def get_data_frame(data) -> pd.DataFrame:
    
    # Convert get_data_list into to data frame
    
    

    # Convert list of data to dataFrame and return DataFrame
    df = pd.DataFrame(data)

    # Extract wanted tags
    df = df[['category', 'sink_method', 'source_method']]
    return df


if __name__ == '__main__':
    data = get_data()
    df = get_data_frame(data)

    # Top 5 Sink methods with findings counts:
    print('\n Top 5 sink methods with finding count:')
    sink_df = pd.DataFrame(df.sink_method.value_counts().nlargest(5))
    sink_df = sink_df.rename(columns={'sink_method': 'findings_count'}).reset_index().rename(
        columns={'index': 'sink_method'})
    print(sink_df)

    # Top 5 source methods with categories and findings counts:
    source_df = pd.DataFrame(df.groupby(['category']).source_method.value_counts().nlargest(5))
    source_df = source_df.rename(columns={'source_method': 'findings_count'}).reset_index()
    print('\n Top 5 source methods with categories and finding count:')
    print(source_df)