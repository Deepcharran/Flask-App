from flask import Flask, render_template, jsonify
import numpy as np
application = Flask(__name__)

random_decimal = np.random.rand()
@application.route('/update_decimal', methods=['POST'])
def updatedecimal():
	random_decimal = np.random.rand()
	return jsonify('', render_template('random_decimal_model.html', x=random_decimal))

@application.route('/')
def homepage ():
	return render_template('home.html', x=random_decimal)
application. run()