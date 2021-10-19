from flask import Flask, render_template, request, redirect, session, flash, jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('algunawea.html')

@app.route('/revisar', methods=['POST'])
def check():
    pass


@app.route('/signin.html')
def signin():
    return render_template('/signin.html')

@app.route('/signup.html')
def signup():
    return render_template('/signup.html')

if __name__ == "__main__":
    app.run(debug=True)
