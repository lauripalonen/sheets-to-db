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
        click.echo("File already exists in the directory. Please choose a unique name for database.")
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
    table_name = raw_input("Give name for the database table: ")
    
    sql_create_table_stmt = "CREATE TABLE IF NOT EXISTS {} (id integer PRIMARY KEY AUTOINCREMENT);".format(table_name)

    try:
        c = conn.cursor()
        c.execute(sql_create_table_stmt)
        print("Table succesfully initiated")

    except Error as e:
        print(e)

    for header in headers:        
        sql_add_column_stmt = " ALTER TABLE {} ADD {} VARCHAR;".format(table_name, header)
        
        try:
            c = conn.cursor()
            c.execute(sql_add_column_stmt)
        except Error as e:
            print(e)
    
    print("columns created")

    populate_table(conn, worksheet, headers, table_name)

def populate_table(conn, worksheet, headers, table_name):
    sql_values = ""

    for row in range (1, worksheet.nrows):
        row_values = "("

        for col in range (0, worksheet.ncols):
            row_values += "'{}', ".format((worksheet.cell(row, col).value).encode('utf-8'))

        row_values = "{})".format(row_values[:-2])
        sql_values += "{}, ".format(row_values)

    sql_values = sql_values[:-2]

    header_values = ', '.join(headers)

    print("HEADER VALUES: {}".format(header_values))

    sql_insert_rows_stmt = "INSERT INTO {} ({}) VALUES {};".format(table_name, header_values, sql_values)

    try:
        c = conn.cursor()
        c.execute(sql_insert_rows_stmt)
        conn.commit()
        print("Table succesfully populated.")
    except Error as e:
        print(e)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection closed")

if __name__ == "__main__":
    main()
