INPUT_FILE = '/home/deepakt/Downloads/fields_with_blanks_and_nulls.txt'

SQL_TEMPLATE = "UPDATE staging.{table_name} SET {column_name} = NULL WHERE {column_name} = '';"


def main():
    with open(INPUT_FILE) as fh:
        tn = ''
        for line in fh:
            l_table_column = line.strip().split('.')
            table_name = l_table_column[0]
            column_name = l_table_column[1]
            if tn != table_name:
                print 'COMMIT;'
                tn = table_name
            print SQL_TEMPLATE.format(table_name=table_name, column_name=column_name)
        print 'COMMIT;'

if __name__ == '__main__':
    main()