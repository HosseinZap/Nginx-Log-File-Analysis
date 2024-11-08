# Log File Analysis and Visualization Using Data Pipeline

- **Project description**

  This project involves creating a data pipeline which parses an input nginx log file in .txt extension, cleans parsed data and imports it to a MySQL database.

  The goal is to use this pipeline as a deployment tool to format the proper framework for extracting insights and generating visualizations from the data.

  ## Defining Steps

  Steps below are essential to prepare the environment for data analysis:

  > 1.  Write a Python script that parses the input file, extracts relevant fields and writes them to a temporary csv file.

  > 2.  Write a Python script to clean the parsed data and remove/replace missing values.

  > 3.  Write a Python script to import the data into a MySQL database.
  > 4.  Generate visualizations and analyze the data

  ## How Parser Works

  The `log_parser.py` script consists of a `main()` function and a `parse()` function.

  The idea behind parsing process is to match each row of the log file with a regex (regular language) phrase so we will be able to extract values from the valid lines that comply with the standard format defined in the `main()` and passed to the `parse()`.
  To do so, the Python `re` module is used to compile the regex phrase.
  To mention the format of the nginx log, an example is:

  `74.240.191.221 - - [25/Jun/2024:00:06:22 +0000] "DELETE /index.html?product_id=585&user_id=218 HTTP/1.1" 200 1974`

  There are other information in a nginx log file like Referrer and User Agent, although in our case we're only interested in sections "IP", "Timestamp", "Request Method", "URL", "Status Code", "Response Size (in bytes)" and "Query Parameters", so the proper regex that explains this specific pattern would be like:

  ```py
   (\S+) - - \[(.*?)\] "(.*)" (\d+) (\d+)
  ```

  which will suffice our purpose.

  Further on, a temporary csv file called `test.csv` is created in the same directory to be the destination of the extracted data.

  Inside the `parse()`, both `test.csv` and input file are opened in the write and read mode respectively. The first row that is written to the csv file is the column row, following by each line of the parsed txt file that has matched with the log format.

  The values `ip`, `timestamp`, `req`, `status` and `size` are assigned with the corresponding extracted values from the log line using `groups()` method.

  The `date` object is defined to hold the datetime object created from the `timestamp` string using `datetime.strptime()` method.

  Moreover, query parameters are extracted from the URL and finally, all values are written to the csv file as a whole record.

  As we see, the main goal of the parsing is indeed satisfied here and next steps are related to cleaning and importing processes which we'll cover.

  ## Cleaning Data

  In this section, we are only interested in missing values that are represented by "NULL" in the log file. After executing `clean.py` we can see that all missing values reside in the "IP" column only, which implies the essence of replacing them with some meaningful value, such as "0.0.0.0" in this case, to be a reflection of an unknown IP address.

  In `clean.py`, the first operation was to create a Pandas DataFrame object from `test.csv`, to become prepared for NULL value replacement.

  Before filling NULL values with "0.0.0.0", we should replace the actual Pandas NAN value with the "NULL" string stored in the targeted cells using `replace("NULL", pd.NA)` method in this case.

  Finally, we can use `fillna()` method from Pandas to detect and replace NAN values with "0.0.0.0".

  The result is then stored in another csv file called `cleaned.csv` in the same directory for further operations.

  ## Deployment

  To import data to a MySQL database, we need to follow these steps:

  > 1.  Connect to the database

  > 2.  Create a table with required columns

  > 3.  Insert all rows from `cleaned.csv` to the table

  In `deploy_db.py`, required connection parameters are specified and passed by the user to the program.

  > The database should be declared before executing the script.

  Python `mysql` module is used to connect and query the MySQL database, so ensure you have it installed using:

  ```cmd
   pip install mysql-connector-python
  ```

  Further on, the program connects to the desired database and creates a table with the name specified by user. If connection information were false, an error occurs indicating that there's a potential problem with connection establishment.

  The query:

  ```sql
  CREATE TABLE {db_name}.{table_name} (id INT AUTO_INCREMENT PRIMARY KEY, ip VARCHAR(16), timestamp TIMESTAMP, request_method VARCHAR(10), url VARCHAR(255), status INT, response_size INT, query_parameters VARCHAR(255));
  ```

  is then executed on the database using the `mysql` cursor object.

  After creating table, the turn is given to the importation operation, but before doing so, the `cleaned.csv` in which our data is stored should be read, the metadata should be skipped and each row should be inserted to the table by executing the following query:

  ```sql
  INSERT INTO {db_name}.{table_name} (ip, timestamp, request_method, url, status, response_size, query_parameters) VALUES (%s, %s, %s, %s, %s, %s, %s);
  ```

  After the process is done, changes are saved to the database with `commit()` method of the `mysql`, and the connection is closed.

  So far, we have seen that our three main goals are satisfied, and the data should be ready for extracting insights and analysis, so next steps will cover what we learned from data by visualization.

  ## Visualization

  These are some ideas for extracting insights from this log data:

  > 1.  Request volume over time
  > 2.  Distribution of status codes
  > 3.  IP addresses with the most number of requests
  > 4.  Distribution of response sizes
  > 5.  The most popular URLs

  In `visualization.ipynb`, we connect to the database again with the help of `mysql` and create a Pandas DataFrame from the table to plot all of these visualizations.

* **Request Volume**

  As the time series plot implies, the peak of the request volume has happened twice, one being around last hours of June 20 and first hours of June 21, and the other one around noon of June 26, with 14 requests.

  We can see, the request volume has growed overall, which means proper considerations should be taken into account for the web server to not become overwhelmed by the potential traffic of requests in future.

* **Distribution of Status Codes**

  The distribution of status codes and contribution percentage of codes "302", "301" and "404" could indicate that there has been probably a change in the resources structure of the web server which has reflected by these two codes occurring pretty often.

  Furthermore, the occurrence of the code "500" which indicates the internal server error is considerable, suggesting the fact that in general, the server need to be more stable in case of the hardware and software performance in future.

* **Top 10 Ip Addresses**

  By referring to the number of requests done by the top 10 Ip addresses, It's explicit that nearly twice the amount of requests made by the second Ip address is related to unknown Ip addresses, which is definitely not a positive sign from security perspective, to mention one from several other concerns.

* **Distribution of Response Sizes**

  The distribution of response sizes doesn't follow a normal distribution, which means larger contents are affecting server's performance. This could be overcome by ensuring the server is usually sending contents of the same size. This will definitely enhance the performance of the server.

* **Top 10 Popular URLs**

  This chart only makes sense, when used to inform developers of which resource objects are requested more overally. This can help developers to plan for future policies on the way these resources are stored on the web server, for example.

  ## Potential Improvements

  This project has several shortcomings that should be fixed in future:

  > - There was less focus on the code design
  > - Less considerations were taken into account in the case of exception handling which should be fixed
  > - More valuable and deeper insights could be made of this data
  > - This project was based on the nginx log file in `.txt` format, which is not very realistic or practical in work environment, especially because nginx log files follow `.log` extension

  It is appreciated that the reader consider this project as an internship project.

  Further comments and suggestions for bug fixes or better code design, as well as innovative ideas for insight extraction are all appreciated.
