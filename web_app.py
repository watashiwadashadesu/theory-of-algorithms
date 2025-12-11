from flask import Flask, render_template, jsonify, request
import json
import sys
import os

# Добавляем путь к модулям
sys.path.append('/app')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/compute', methods=['POST'])
def compute():
    data = request.json
    # Здесь вызываешь твой вычислитель
    from core.evaluator import Evaluator
    from core.function_factory import create_addition

    evaluator = Evaluator()
    add_func = create_addition()
    result = evaluator.evaluate(add_func, data['args'])

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)