import mysql.connector
import mysql
import csv
import os


def main(db_username, db_password, db_host, db_name, table_name):

    # connects to the database
    try:
        db = mysql.connector.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        database=db_name
        )
    except:
        print("connection with database failed")
        return

    # cursor object to use in executing queries
    cursor = db.cursor()

    # SQL query to create a table with the specific name the user has indicated
    create_table = f"CREATE TABLE {db_name}.{table_name} (id int auto_increment primary key, ip varchar(16), timestamp timestamp, request_method varchar(10), url varchar(255), status int, response_size int, query_parameters varchar(255));"

    cursor.execute(create_table)

    # opens the cleaned.csv file to read from and import in the table rows
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csvfile = os.path.join(current_directory, "cleaned.csv")    
    with open(csvfile, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # SQL query for data insertion in the table
            insert_record = f"INSERT INTO {db_name}.{table_name} (ip, timestamp, request_method, url, status, response_size, query_parameters) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_record, row)

    db.commit()     # applies changes

    # closes the connection
    cursor.close()
    db.close()

    print("deployment done")


if __name__ == "__main__":

    # receives input parameters from the user for the database connection process
    try:
        db_username = input("> username: ")
        db_password = input("> password: ")
        db_host = input("> host: ")
        db_name = input("> database name: ")
        table_name = input("> table name: ")
        main(db_username, db_password, db_host, db_name, table_name)
    except:
        print("invalid input or table already exists")