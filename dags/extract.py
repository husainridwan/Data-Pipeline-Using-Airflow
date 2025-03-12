import json
import requests

def extract_zillow_data(**kwargs):
    url = kwargs['url']
    headers = kwargs['headers']
    querystring = kwargs['querystring']
    dt_string = kwargs['date_string']

    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()

    # Specify the output file path
    output_file_path = f"/home/ubuntu/response_data_{dt_string}.json"
    file_str = f'response_data_{dt_string}.csv'

    # Write the JSON response to a file
    with open(output_file_path, "w") as output_file:
        json.dump(response_data, output_file, indent=4)
    
    output_list = [output_file_path, file_str]
    return output_list   