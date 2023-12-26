import csv

# Read the data from the text file
with open('3_script_output.txt', 'r') as file:
    data = file.read()

# Split the data into lines
lines = data.split('\n')

# Open a CSV file for writing
with open('jenkins_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write the header
    csvwriter.writerow(['Build Number', 'Timestamp', 'Result'])

    # Parse the data and write to CSV
    for line in lines:
        if 'Build Number' in line:
            build_number = line.split(': ')[-1]
        elif 'Timestamp' in line:
            timestamp = line.split(': ')[-1]
        elif 'Result' in line:
            result = line.split(': ')[-1]
            csvwriter.writerow([build_number, timestamp, result])
