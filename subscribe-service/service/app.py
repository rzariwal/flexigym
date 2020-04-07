from flask import Flask, request, redirect, url_for
import setup

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/add")
def addToOrder():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:



        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))


# from project setup reference
app = setup.create_app()

if __name__ == '__main__':
    app.run()
