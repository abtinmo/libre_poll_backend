from sanic.blueprints import Blueprint
from sanic.response import json 
from db.insert import insertUser
from db.query import getToken

bp = Blueprint('view_user')


@bp.route("/")
async def main(request):
    return json({"hello":"main"})


@bp.route("/adduser" , methods=["POST"])
async def adduser(request):
    """
    adds user to database 
    {"username":"example" ,
    "password":"examplepassword" ,
    "email":"email@email.com"}
    """
    return insertUser(request.json)


@bp.route("/gettoken" , methods=["GET"])
def getToken(request):
    print(request.json)
    return  getToken(request.json)


