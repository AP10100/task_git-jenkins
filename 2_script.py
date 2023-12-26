import requests
from datetime import datetime

def convert_timestamp(timestamp):
    # Convert Unix timestamp to human-readable format
    return datetime.utcfromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S UTC')

def get_all_branches(job_name, api_token, jenkins_url, file):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    url = f'{jenkins_url}/job/{job_name}/api/json?tree=jobs[name]'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        branches = [job['name'] for job in data.get('jobs', [])]

        for branch in branches:
            get_build_info(job_name, branch, api_token, jenkins_url, file)
    else:
        print(f'Error fetching branch information for {job_name}. Status code: {response.status_code}')

def get_build_info(job_name, branch_name, api_token, jenkins_url, file):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    url = f'{jenkins_url}/job/{job_name}/job/{branch_name}/api/json?tree=builds[number,timestamp,result]'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        builds = data.get('builds', [])

        file.write(f'\n=== {job_name}/{branch_name} ===\n')
        
        for build in builds:
            build_number = build.get('number')
            timestamp = build.get('timestamp')
            result = build.get('result', 'UNKNOWN')

            file.write(f'Build Number: {build_number}\n')
            file.write(f'Timestamp: {convert_timestamp(timestamp)}\n')
            file.write(f'Result: {result}\n')
            file.write('\n')
    else:
        print(f'Error fetching build information for {job_name}/{branch_name}. Status code: {response.status_code}')

# Replace these values with your Jenkins API token, URL, and multibranch job name
api_token = '111a78a4b320267b90f5c4ff96044ac134'
jenkins_url = 'https://cicdxc.arlocloud.com/'
job_name = 'CI-Cloud'  # Replace with your multibranch job name

with open('2_script_output.txt', 'w') as output_file:
    get_all_branches(job_name, api_token, jenkins_url, output_file)
