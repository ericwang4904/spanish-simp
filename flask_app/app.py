import flask
from flask import Flask, render_template, request
import jinja2

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/parse', methods=['POST'])
def parse():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('result.html', user_input=user_input)
    
if __name__ == "__main__":
    app.run(debug=True)  # change to false afterwards