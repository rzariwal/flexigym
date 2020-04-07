from flask import Flask

import setup

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# from project setup reference
app = setup.create_app()

if __name__ == '__main__':
    app.run()
