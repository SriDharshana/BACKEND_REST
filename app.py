import psycopg2
from urllib.parse import unquote
from flask import Flask, jsonify, request

app = Flask(_name_)

# Function to establish a connection to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="bank_data",
        user="your_username",
        password="your_password"
    )
    return conn

# Search API to return possible matches across all columns and all rows, ordered by IFSC code (ascending order) with limit and offset.
@app.route('/api/search', methods=['GET'])
def search():
    # Get query parameters from the request
    search_query = unquote(request.args.get('q', ''))
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    # Establish a connection to the database
    conn = connect_to_db()

    # Query the database for matching records
    cur = conn.cursor()
    cur.execute("SELECT * FROM bank_branches WHERE LOWER(CONCAT_WS(' ', bank_name, branch_name, address, city, district, state)) LIKE %s ORDER BY ifsc ASC LIMIT %s OFFSET %s", ('%'+search_query.lower()+'%', limit, offset))
    rows = cur.fetchall()

    # Close the database connection
    cur.close()
    conn.close()

    # Return the matching records as a JSON response
    return jsonify({'result': rows})

# Branch API to return possible matches based on the branch name ordered by IFSC code (descending order) with limit and offset
@app.route('/api/branch', methods=['GET'])
def branch():
    # Get query parameters from the request
    search_query = unquote(request.args.get('q', ''))
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    # Establish a connection to the database
    conn = connect_to_db()

    # Query the database for matching records
    cur = conn.cursor()
    cur.execute("SELECT * FROM bank_branches WHERE LOWER(branch_name) LIKE %s ORDER BY ifsc DESC LIMIT %s OFFSET %s", ('%'+search_query.lower()+'%', limit, offset))
    rows = cur.fetchall()

    # Close the database connection
    cur.close()
    conn.close()

    # Return the matching records as a JSON response
    return jsonify({'result': rows})