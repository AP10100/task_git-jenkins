import requests
from urllib.parse import unquote  # Import unquote function 

def delete_build(api_token, jenkins_url, job_name, build_number):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    url = f'{jenkins_url}/job/{job_name}/{unquote(str(build_number))}/doDelete'

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print(f'Successfully deleted build {build_number} for job {job_name}')
    else:
        print(f'Error deleting build {build_number} for job {job_name}. Status code: {response.status_code}')

# Replace these values with your Jenkins API token, URL, job name, and build number
api_token = '111e7343a1d813c7cc6dd8d158d2d9ebd4'
jenkins_url = 'http://localhost:8080/'
job_name = 'tetsing_delete/main'
build_number = '2'

delete_build(api_token, jenkins_url, job_name, build_number)
