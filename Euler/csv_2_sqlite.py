#######################################
# file: csv_2_sqlite                  #
# Author : Anil Pratap Singh          #
#######################################


import sys
import sqlite3
    
def csv_2_sqlite(fileIn,fileSQL,tabName,
                headersL = None, separator = ',',
                verbose = 1
                ):
    file_in = None
    
    try:
        conn = sqlite3.connect(fileSQL)
        #Clear If table with this name exists.
        conn.execute('''
        DROP TABLE IF EXISTS ?tabName?
        '''.replace('?tabName?',tabName)
        )
        
        #Lets make a create statement.
        file_in = open(fileIn,'r')
        
        if headersL == None:
            headersL = file_in.readline().split(separator)
            headersL = [col.strip() for col in headersL]
            if verbose == True:
                print (headersL)
        
        headers = ',\n'.join([col+' TEXT' for col in headersL])
        
        create_table_sql = '''
        CREATE TABLE ?tabName? (
        ?headers?
        )'''.replace('?headers?',headers).replace('?tabName?',tabName)
        
        #Creating a schema.
        conn.execute(create_table_sql)
        
        #Now let us fill the table from the file.
        insert_sql = '''INSERT INTO ?tabName? VALUES (?record?)'''
        insert_sql = insert_sql.replace('?tabName?',tabName)
        
        conn.execute('PRAGMA synchronous=OFF');
        for line in file_in:
            if verbose == True:
                print (line)
                
            sqli = insert_sql.replace('?record?',line.replace('\n',''))
            conn.execute(sqli)
        conn.commit()
        
        return conn
        
    except Exception as err:
        sys.stderr.write(("ERROR ('read_data'):  %s\n") % str(err))
    finally:
        try:
            file_in.close()
        except Exception as err:
            pass
        
