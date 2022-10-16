from flask import Flask
import numpy as np
import pandas as pd
import time
from datetime import datetime
import math

app = Flask(__name__)
@app.route('/')
def numpy_pack():
    a = np.array([[1, 2],[3, 4]])
    b = np.array([[4, 3],[2, 1]])
    return str(a.dot(b))

@app.route('/pandas')
def pandas_pack():
    data = np.array(['g', 'e', 'e', 'k', 's'])
    ser = pd.Series(data)
    return dict(ser)

@app.route('/time')
def time_pack():
    curr = time.ctime(time.time())
    return curr

@app.route('/datetime')
def datetime_pack():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

@app.route('/math')
def math_pack():
    sqroot = math.sqrt(25)
    return str(sqroot)

if __name__ == '__main__':
    app.run(debug = True)