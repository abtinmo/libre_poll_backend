from sanic.blueprints import Blueprint
from sanic.response import json , text
from db.insert import insertUser , setEmail  , addPoll , doVote , editPoll
from db.query import getToken , userExists , emailExists , getPolls , getPoll , getVote , getVotes
from db.delete import removeUser , removePoll
bp = Blueprint('view_user')



@bp.route("/getvotes" , methods=["POST"])
async def getvotes(request):
    token = request.headers.get('token')
    return getVotes( token )


@bp.route("/getvote" , methods=["POST"])
async def getvote( request ):
    token = request.headers.get('token')
    return getVote(token , request.json)


@bp.route("/vote" , methods=["POST"])
async def vote(request):
    """
    gets  poll_id , and list of choosen options.
    """
    token = request.headers.get('token')
    return doVote(token , request.json)

@bp.route("/removepoll" , methods=["POST"])
async def removepoll(request):
    """
    deletes the poll request of user 
    """
    token = request.headers.get('token')
    return removePoll(token , request.json)


@bp.route("/getpoll" , methods=["POST"] )
async def getpoll(request):
    token = request.headers.get('token')
    return getPoll(token , request.json)


@bp.route("/getpolls" , methods=["POST"])
async def getpolls(request):
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


@bp.route("/editpoll" , methods=["POST"])
async def editpoll(request):
    """
   get uuid and poll information and update poll
    """
    token = request.headers.get('token')
    return editPoll(token , request.json)

