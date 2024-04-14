from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def open():
    return render_template('index.html')

@app.route('/profile')
def about():
    return render_template('about.html')

@app.route('/about')
def services():
    return render_template('services.html')





if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080")