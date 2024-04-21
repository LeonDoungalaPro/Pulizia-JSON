from flask import Flask, render_template, request

import os
import sys


current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))


sys.path.append(parent_path)

from PuliziaJSON import DataCleaner

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        input_string = request.form['input']
        final_clean_json = DataCleaner(input_string)
        if final_clean_json:
            return render_template('result.html', result=final_clean_json)
        else:
            return "Error: Data is empty."
    else:
        return "Method Not Allowed"

if __name__ == '__main__':
    app.run(debug=True)
