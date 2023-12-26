# import requests

# # Replace these variables with your Jenkins server details
# jenkins_url = 'https://cicdxc.arlocloud.com/'
# api_token = '111a78a4b320267b90f5c4ff96044ac134'

# import requests

# def get_build_info(job_name, branch_name, api_token, jenkins_url):
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {api_token}'
#     }

#     url = f'{jenkins_url}/job/{job_name}/job/{branch_name}/api/json?tree=builds[number,timestamp,result]'

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         builds = data.get('builds', [])

#         with open(f'{job_name}_{branch_name}_build_info.txt', 'w') as file:
#             for build in builds:
#                 build_number = build.get('number')
#                 timestamp = build.get('timestamp')
#                 result = build.get('result', 'UNKNOWN')

#                 file.write(f'Build Number: {build_number}\n')
#                 file.write(f'Timestamp: {timestamp}\n')
#                 file.write(f'Result: {result}\n')
#                 file.write('\n')
#     else:
#         print(f'Error fetching build information for {job_name}/{branch_name}. Status code: {response.status_code}')

# # Replace these values with your Jenkins API token, URL, and multibranch job name
# api_token = '111a78a4b320267b90f5c4ff96044ac134'
# jenkins_url = 'https://cicdxc.arlocloud.com/'
# job_name = 'hmsfeeds'  # Replace with your multibranch job name

# # Fetch build information for each branch
# branches = ['CICD-7776', 'CICD-7751', 'CICD-7041']  # Replace with your branch names

# for branch in branches:
#     get_build_info(job_name, branch, api_token, jenkins_url)







import requests

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
            file.write(f'Timestamp: {timestamp}\n')
            file.write(f'Result: {result}\n')
            file.write('\n')
    else:
        print(f'Error fetching build information for {job_name}/{branch_name}. Status code: {response.status_code}')

# Replace these values with your Jenkins API token, URL, and multibranch job name
api_token = '111a78a4b320267b90f5c4ff96044ac134'
jenkins_url = 'https://cicdxc.arlocloud.com/'
job_name = 'hmsfeeds'  # Replace with your multibranch job name

# Fetch build information for each branch
branches = ['CICD-7776', 'CICD-7751', 'CICD-7041']  # Replace with your branch names

with open('build_info.txt', 'w') as output_file:
    for branch in branches:
        get_build_info(job_name, branch, api_token, jenkins_url, output_file)
