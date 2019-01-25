from sanic.blueprints import Blueprint
from sanic.response import json , text
from db.insert import insertUser , setEmail  , addPoll
from db.query import getToken , userExists , emailExists , getPolls
from db.delete import removeUser , removePoll
from db.edite import editePoll
bp = Blueprint('view_user')



@bp.route("/removepoll" , methods=["POST"])
async def main(request):
    """
    deletes the poll request of user 
    """
    token = request.headers.get('token')
    return removePoll(token , request.json)


@bp.route("/getpolls" , methods=["POST"])
async def main(request):
    """
    returns all user polls
    """
    token = request.headers.get('token')
    return getPolls(token)


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
    return userExists(request.json)

@bp.route("/emailexists" , methods=["POST"])
async def emailexists(request):
    """
    if email is in database return false
    """
    return emailExists(request.json)


@bp.route("/setemail" , methods=["POST"])
async def setemail(request):
    """
    gets email and decodes the token , updates email for user in database
    """
    token = request.headers.get('token')
    email = request.json['email']
    return setEmail(token , email)


@bp.route("/addpoll" , methods=["POST"])
async def addpoll(request):
    """
    get token and poll information and add poll tp database
    """
    token = request.headers.get('token')
    json = request.json
    return addPoll(token , json)


@bp.route("/removeuser" , methods=["POST"])
async def removeuser(request):
    """
    validates user with token , and remose user
    """
    token = request.headers.get('token')
    return removeUser(token)


@bp.route("/editepoll" , methods=["POST"])
async def editepoll(request):
    """
   get uuid and poll information and update poll
    """
    token = request.headers.get('token')
    return editePoll(token , request.json)

