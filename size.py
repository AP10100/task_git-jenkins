
import requests

# Replace 'YOUR_JENKINS_URL' and 'YOUR_JOB_NAME' with your Jenkins URL and job name
JENKINS_URL = "http://localhost:8080/"
JOB_NAME = "sample_multibranch"

def get_branch_info(branch_name):
    branch_url = f"{JENKINS_URL}/job/{JOB_NAME}/job/{branch_name}/api/json"
    
    try:
        # Fetch information about the branch using the Jenkins API
        response = requests.get(branch_url)
        
        if response.status_code == 200:
            branch_info = response.json()
            return branch_info
        else:
            print(f"Error: Unable to fetch information for branch {branch_name}. Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch information for branch {branch_name}: {e}")
        return None

try:
    # Fetch information about the Multibranch Pipeline job
    job_info_url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json"
    job_info_response = requests.get(job_info_url)

    if job_info_response.status_code == 200:
        job_info = job_info_response.json()

        # Iterate through branches
        for branch_info in job_info.get("jobs", []):
            branch_name = branch_info.get("name")
            
            # Get and print information about each branch
            branch_info = get_branch_info(branch_name)
            if branch_info is not None:
                print(f"Branch Name: {branch_info.get('name')}")
                print(f"Branch URL: {branch_info.get('url')}")
                print(f"Branch Description: {branch_info.get('description')}")
                print("\n")
    else:
        print(f"Error: Unable to fetch job information. Status Code: {job_info_response.status_code}")
except Exception as ex:
    print(f"Error: {ex}")
