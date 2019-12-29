import click
import xlrd
import sqlite3
from sqlite3 import Error
import os

@click.command()
@click.argument('filename')
@click.argument('db_filename')
def main(filename, db_filename):
    if validate_spreadsheet_type(filename) and validate_db_type(db_filename):
        click.echo("Converting \"{}\" into a database \"{}\"".format(filename, db_filename))
        worksheet = get_spreadsheet(filename)
        convert_to_db(worksheet, db_filename)
    else:
        click.echo("Process aborted.")

def validate_spreadsheet_type(filename):
    file_check = os.path.exists(filename)

    if not file_check:
        click.echo("No such spreadsheet file.")
        return False

    if not filename.endswith('.xlsx'):
        click.echo("Invalid spreadsheet file type (.xlsx required).")
        return False
    
    return True

def validate_db_type(db_filename):
    if os.path.exists(db_filename):
        click.echo("File already exists in the directory. Please choose unique name for database.")
        return False

    if not db_filename.endswith('.db'):
        click.echo("Invalid database file type (.db required).")
        return False
    
    return True

def get_spreadsheet(filename):
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    return worksheet
    num_cols = worksheet.ncols
    num_rows = worksheet.nrows

    if num_cols == 0 or num_rows == 0:
        print("Your spreadsheet is empty")


    print("Your spreadsheet contains {} columns and {} rows".format(num_cols, num_rows))

    user_input = raw_input("Use first row as headers for database columns? [y/n] ")

    if user_input == 'y':
        print("You selected yes.")
    elif user_input == 'n':
        print("You selected no.")
    else:
        print("Invalid input.")

def convert_to_db(worksheet, db_filename):
    num_cols = worksheet.ncols
    num_rows = worksheet.nrows

    print("Your spreadsheet contains {} columns and {} rows".format(num_cols, num_rows))

    user_input = raw_input("Use first row as headers for database columns? [y/n] ")

    headers = []

    if user_input == 'y':
        for col_idx in range(0, num_cols):
            title = worksheet.cell(0, col_idx).value
            headers.append(title)

        print("using first row as headers for columns")

    elif user_input == 'n':
        print("Rename columns for database: ")
        for col_idx in range(0, num_cols):
            title = worksheet.cell(0, col_idx).value
            user_input = raw_input("Column {} ('{}'): ".format(col_idx, title))
            headers.append(user_input)

    print("Creating database file...")
    conn = create_connection(db_filename)
    
    if conn is not None:
        create_table(conn, worksheet, headers)

def create_connection(db_filename):
    conn = None
    try:
        conn = sqlite3.connect("./{}".format(db_filename))
        print("Database succesfully initiated")
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, worksheet, headers):
    user_input = raw_input("Give name for the database table: ")
    
    sql_create_table_stmt = " CREATE TABLE IF NOT EXISTS {} (id integer PRIMARY KEY);".format(user_input)

    try:
        c = conn.cursor()
        c.execute(sql_create_table_stmt)
        print("Table succesfully initiated")

    except Error as e:
        print(e)

    for header in headers:        
        sql_add_column_stmt = " ALTER TABLE {} ADD {} VARCHAR;".format(user_input, header)
        
        try:
            c = conn.cursor()
            c.execute(sql_add_column_stmt)
        except Error as e:
            print(e)
    
    print("columns created")

if __name__ == "__main__":
    main()
