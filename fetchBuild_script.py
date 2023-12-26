import requests
from datetime import datetime, timedelta
from urllib.parse import unquote  # Import unquote function 

def convert_timestamp(timestamp):
    # Convert Unix timestamp to human-readable format
    return datetime.utcfromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S UTC')

def is_older_than_six_months(timestamp):
    # Check if the build timestamp is older than 6 months
    six_months_ago = datetime.utcnow() - timedelta(days=1)
    build_time = datetime.utcfromtimestamp(timestamp / 1000.0)
    return build_time < six_months_ago

def get_all_multibranch_jobs(api_token, jenkins_url, file):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    url = f'{jenkins_url}/api/json?tree=jobs[name]&xpath=//job[contains(name,%27MultiBranch%27)]'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        multibranch_jobs = [job['name'] for job in data.get('jobs', [])]

        for job_name in multibranch_jobs:
            get_all_branches(job_name, api_token, jenkins_url, file)
    else:
        print(f'Error fetching multibranch job information. Status code: {response.status_code}')

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

        file.write(f'\n==== {job_name}//{unquote(branch_name)} ====\n')
    
        for build in builds:
            build_number = build.get('number')
            timestamp = build.get('timestamp')
            result = build.get('result', 'UNKNOWN')

            if is_older_than_six_months(timestamp):
                file.write(f'Build Number: {build_number}   ')
                file.write(f'Timestamp: {convert_timestamp(timestamp)}   ')
                file.write(f'Result: {result}   ')
                file.write('\n')                        
    else:
        print(f'Error fetching build information for {job_name}/{branch_name}. Status code: {response.status_code}')

# Replace these values with your Jenkins API token, URL, and multibranch job name
api_token = '1132aa14cf15cdf624ea0a9f71a3b8d591'
jenkins_url = 'https://cicdxc.arlocloud.com/'

with open('fetchBuild_script_output.txt', 'w') as output_file:
    get_all_multibranch_jobs(api_token, jenkins_url, output_file)
