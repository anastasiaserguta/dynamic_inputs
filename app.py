from os import environ
from psycopg2 import connect, sql
from flask import Flask, render_template, request, jsonify
import json


app = Flask(__name__)
app.config['DEBAG'] = True

def get_db_connect():
    conn = connect(host='localhost',
                    database=environ['POSTGRES_DB'],
                    user=environ['USERNAME_DB'],
                    password=environ['PASSWORD_DB'])
    return conn

@app.route('/')
def start_app():
    return render_template('inputs.html')



@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()
    try:
        # Подключение к базе данных PostgreSQL
        conn = get_db_connect()
        cursor = conn.cursor()
        
        # Вставка данных в базу
        for inp in data:
            cursor.execute('INSERT INTO Inputs (data) VALUES (%s)', (json.dumps(inp['value'],),))
        
        # Сохранение изменений и закрытие соединения
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'status': 'success', 'redirect_url': '/all_data'}), 200

    except Exception as e:
        print(f'Произошла ошибка при добавлении данных: {e}')
        return jsonify({'status': 'error'}), 500


def get_data_from_db():
    try:
        # Подключаемся к базе данных
        conn = get_db_connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Inputs;') 
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f'Произошла ошибка при получении данных из базы: {e}')
        return []

@app.route('/all_data')
def all_data_from_db():
    all_inputs = get_data_from_db()
    return render_template('submit.html', data=all_inputs)




