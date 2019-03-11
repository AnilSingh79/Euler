#######################################
# File: Euler                         #
# Author : Anil Pratap Singh          #
#######################################

import sys

#A function to obtain column names.
def get_column_names(conn,tabName):
    try:
        sql = "PRAGMA table_info (?tabNam?)".replace('?tabNam?',tabName)
        cursor = conn.cursor()
        cursor.execute(sql)
        tab_info = cursor.fetchall()
        col_nams = [i_info[1] for i_info in tab_info]
        col_type = [i_info[2] for i_info in tab_info]
        return col_nams,col_type
    except Exception as err:
        sys.stderr.write(("ERROR ('read_data'):  %s\n") % str(err))

#Get a list of ROWS with a SELECT query
def get_bysql(query,conn,verbose=False):
    'Returns list of lists data fetched by query rowXcolumns format'
    try:
        #query = query.replace('?srcName?',tabName)
        if verbose==True : print (query)
        results = conn.cursor().execute(query)
        dataSet = []
        for r in results:
            rList = list(r)
            dataSet.append(rList)
        return dataSet  
    except Exception as err:
        sys.stderr.write(("ERROR ('get_bysql'):  %s\n") % str(err))
        sys.stderr.write ("\n\n****Exception Encountered****\n")
        sys.stderr.write ('Not Happy With \n'+query)
     
#Get a list of COLUMNS with a SELECT query
def get_ncols_bysql(query,n,conn,verbose=False):
    'Returns list of lists data fetched by query in columnXrow format'
    try:
        if n==1 : return get_1col_bysql(query, conn)
        res = get_bysql(query,conn,verbose=verbose)
        data_cols = []
        for i in range(0,n):    
            data_cols.append([line[i] for line in res])
        return tuple(data_cols)
    except Exception as err:
        sys.stderr.write(err,'euler.get_ncols_bysql')
        
