import click
import xlrd
from DAO import Dao
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

def convert_to_db(worksheet, db_filename):

    click.echo("Creating database file...")
    new_dao = Dao(db_filename)
    conn = new_dao.create_connection()
    
    if conn is not None:
        table_name = raw_input("Give name for the database table: ")
        columns = get_headers(worksheet)
        values = get_values(worksheet)

        new_dao.create_table(table_name)
        
        for column in columns:
            new_dao.create_column(table_name, column)

        column_titles = ', '.join(columns)

        new_dao.insert_values(table_name, column_titles, values)

    conn.close()

def get_headers(worksheet):
    num_cols = worksheet.ncols
    num_rows = worksheet.nrows

    click.echo("Your spreadsheet contains {} columns and {} rows".format(num_cols, num_rows))
    user_input = raw_input("Use first row as headers for database columns? [y/n] ")

    headers = []

    if user_input == 'y':
        click.echo("using first row as headers for columns")

        for col_idx in range(0, num_cols):
            header = worksheet.cell(0, col_idx).value
            headers.append(header)
    
    elif user_input == 'n':
        click.echo("Rename column headers for database: ")
        for col_idx in range(0, num_cols):
            header_old = worksheet.cell(0, col_idx).value
            header_new = raw_input("Column {} ('{}'): ".format(col_idx + 1, header_old))
            headers.append(header_new)

    return headers



def get_values(worksheet):
    values = ""

    for row in range (1, worksheet.nrows):
        row_values = "("

        for col in range (0, worksheet.ncols):
            row_values += "'{}', ".format((worksheet.cell(row, col).value).encode('utf-8'))

        row_values = "{})".format(row_values[:-2])
        values += "{}, ".format(row_values)

    values = values[:-2]

    return values

if __name__ == "__main__":
    main()
