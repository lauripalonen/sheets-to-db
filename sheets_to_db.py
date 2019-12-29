import click
import xlrd

@click.command()
@click.argument('filename')
@click.argument('db_filename')
def main(filename, db_filename):
    if validate_spreadsheet_type(filename) and validate_db_type(db_filename):
        click.echo("Converting \"{}\" into a database \"{}\"".format(filename, db_filename))
        read_spreadsheet(filename)
    else:
        click.echo("process aborted.")

def validate_spreadsheet_type(filename):
    if not filename.endswith('.xlsx'):
        click.echo("invalid spreadsheet file type (.xlsx required).")
        return False
    return True

def validate_db_type(db_filename):
    if not db_filename.endswith('.db'):
        click.echo("invalid database file type (.db required).")
        return False
    return True

def read_spreadsheet(filename):
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    num_cols = worksheet.ncols
    num_rows = worksheet.nrows

    print("Your spreadsheet contains {} columns and {} rows".format(num_cols, num_rows))

    user_input = raw_input("Use first row as headers for database columns? [y/n] ")

    if user_input == 'y':
        print("You selected yes.")
    elif user_input == 'n':
        print("You selected no.")
    else:
        print("Invalid input.")

if __name__ == "__main__":
    main()
