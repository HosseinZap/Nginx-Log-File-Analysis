import re
import csv
from datetime import datetime 
import os


def parse(line_format, input_file, output_file):
    try:
        with open(output_file, "w") as csvfile:     # opens the temporary csv file in write mode
            writer = csv.writer(csvfile)
            writer.writerow(["IP", "Timestamp", "Request method", "URL", "Status", "Response size(bytes)", "Query parameter(s)"])       # defines columns
            file = open(input_file, "r", encoding="utf-8")     # opens log file in read text mode
            for line in file:
                is_match = line_format.match(line)      # matches each line that satisfies the standard format of the nginx log file

                if is_match:
                    ip, timestamp, req, status, size = is_match.groups()        # extracts required values from the line
                    date = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')     # casts the timestamp string to a datetime object for easier handling    
                    method, url = req.split()[0], req.split()[1]    # seperates the request method from the URL

                    # extracts the parameter-value pair from the URL
                    index = url.find("?")
                    q_parameters = url[index + 1:].split("&")

                    writer.writerow([ip, date, method, url, status, size, q_parameters])       # writes the extracted values to the csv file
        print("Process done")
    except:
        print("error occurred during file process")
    return

def main():
    
    # defines a regex to compare and match each log line with
    line_format = re.compile(r'(\S+) - - \[(.*?)\] "(.*)" (\d+) (\d+)')     

    # gets the directory of the current Python script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # creates a file in the same directory as the Python script
    file_path = os.path.join(current_directory, "test.csv")

    # stores input and output files 
    input_file , output_file = input("enter the directory of the log file: ").strip(), file_path
    parse(line_format, input_file, output_file)
    return


if __name__ == "__main__":
    main()



