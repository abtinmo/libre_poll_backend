from sanic import Sanic
from view import bp


app = Sanic()
app.blueprint(bp)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
