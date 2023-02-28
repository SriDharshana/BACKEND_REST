from flask import Flask,request
import json
import psycopg2
import http.server

app = Flask(__name__)

# Possible matches across all columns and all rows, ordered by IFSC code (ascending order) with limit and offset.

@app.route("/api/search")
def search_case():
    connection = psycopg2.connect(
    database="postgres", user='postgres', password='dharshana@16', host='127.0.0.1', port= '5432')
    connection.autocommit = True
    cursor = connection.cursor()
    query1='SELECT ifsc, bank_id, branch, address, city, district, state FROM bank_db WHERE ifsc LIKE CONCAT(%s) OR branch LIKE CONCAT(%s) OR address LIKE CONCAT(%s) OR city LIKE CONCAT(%s) OR district LIKE CONCAT(%s) OR state LIKE CONCAT(%s) OR bank_name LIKE CONCAT(%s) ORDER BY ifsc LIMIT %s OFFSET %s'
    q = '%'+request.args.get("q").upper()+'%'
    args=[q,q,q,q,q,q,q,int(request.args.get("limit")),int(request.args.get("offset"))]
    cursor.execute(query1,args)
    result1 = cursor.fetchall();
    connection.commit()
    connection.close()
    search = []
    for row in result1:
        searches = {'ifsc': row[0],'bank_id': row[1],'branch': row[2],'address': row[3],'city': row[4],'district': row[5],'state': row[6]}
        search.append(searches)
    resultjson1 = {'branches': search}
    resultjson_str1 = json.dumps(resultjson1)
    return resultjson_str1



''' Possible matches based on the branch name ordered by IFSC code (descending order) with limit and offset'''

@app.route("/api/branch")
def branch_case():
   

    connection = psycopg2.connect(
    database="postgres", user='postgres', password='dharshana@16', host='127.0.0.1', port= '5432')

    connection.autocommit = True

    cursor = connection.cursor()

    query='SELECT ifsc,bank_id,branch,address,city,district,state from bank_db WHERE branch LIKE concat(%s) ORDER BY ifsc desc LIMIT %s OFFSET %s'
    q = '%'+request.args.get("q").upper()+'%'
    args=[request.args.get("q"), int(request.args.get("limit")), int(request.args.get("offset"))-1]
    print(args)
    cursor.execute(query,args)
    result = cursor.fetchall();
    connection.commit()
    connection.close()
    branches = []
    for row in result:
        branch = {'ifsc': row[0],'bank_id': row[1],'branch': row[2],'address': row[3],'city': row[4],'district': row[5],'state': row[6]}
        branches.append(branch)
    resultjson = {'branches': branches}
    resultjson_str = json.dumps(resultjson)
    return resultjson_str
