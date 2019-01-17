from sanic import Sanic
from sanic.response import json
from SRC.Functions import *
from view import bp


app = Sanic()
app.blueprint(bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
