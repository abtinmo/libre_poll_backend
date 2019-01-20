from sanic.blueprints import Blueprint
from sanic.response import json , text
from db.insert import insertUser , setEmail
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


@bp.route("/gettoken" , methods=["POST"])
async def gettoken(request):
    """
    if user is in database , retorns token
    """
    return  getToken(request.json)



@bp.route("/userexists", methods=["POST"])
async def userexists(request):
    """
    if user is in database return false
    """
    pass


@bp.route("/emailexists" , methods=["POST"])
async def emailexists(request):
    """
    if email is in database return false
    """
    pass


@bp.route("/setemail" , methods=["POST"])
async def setemail(request):
    """
    gets email and decodes the token , updates email for user in database
    """
    token = request.headers.get('token')
    email = request.json['email']
    return setEmail(token , email) 

        
