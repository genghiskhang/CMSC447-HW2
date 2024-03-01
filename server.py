from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS, cross_origin
from http import HTTPStatus

PORT = 8080
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins":"*"}})
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/api/users/columns", methods=["GET"])
def table_columns():
    try:
        conn = sqlite3.connect("hw2.db")
        cur = conn.cursor()
        res = cur.execute(f"SELECT name FROM pragma_table_info('users')")
        response = jsonify({'table_columns':[column[0] for column in res]})
        cur.close()
        conn.close()
        return response, HTTPStatus.OK.value
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value

@app.route("/api/users", methods=["GET"])
def get_all_records():
    try:
        conn = sqlite3.connect("hw2.db")
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM users")
        records = []
        columns = [column[0] for column in cur.description]
        for row in res:
            r = {}
            for i in range(len(columns)):
                r[columns[i]] = row[i]
            records.append(r)
        response = jsonify({'records':records})
        cur.close()
        conn.close()
        return response, HTTPStatus.OK.value
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value


@app.route("/api/users/<id>", methods=["GET"])
def get_record(id):
    try:
        conn = sqlite3.connect("hw2.db")
        cur = conn.cursor()
        res = cur.execute(f"SELECT * FROM users WHERE id = ?", (id,))
        records = []
        columns = [column[0] for column in cur.description]
        for row in res:
            r = {}
            for i in range(len(columns)):
                r[columns[i]] = row[i]
            records.append(r)
        response = jsonify({'records':records})
        cur.close()
        conn.close()
        return response, HTTPStatus.OK.value
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value

@app.route("/api/users/<id>", methods=["POST"])
def create_record(id):
    try:
        data = request.get_json()
        print(data)
        
        conn = sqlite3.connect("hw2.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (id, name, points) VALUES (?, ?, ?)", (id, data["data"]["name"], data["data"]["points"],))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status":"good insert"}), HTTPStatus.OK.value
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value

@app.route("/api/users/<id>", methods=["PUT"])
def update_record(id):
    try:
        data = request.get_json()
        print(data)
        
        conn = sqlite3.connect("hw2.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, points = ? WHERE id = ?", (data["data"]["name"], data["data"]["points"], id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status":"good update"}), HTTPStatus.OK.value
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value

@app.route("/api/users/<id>", methods=["DELETE"])
def delete_record(id):
    try:        
        conn = sqlite3.connect("hw2.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status":"good delete"}), HTTPStatus.OK.value
    except sqlite3.Error as e:
        return jsonify({'error':str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value

app.run(port=PORT)