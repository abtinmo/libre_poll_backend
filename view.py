from sanic.blueprints import Blueprint
from sanic.response import json , text
from db.insert import insertUser

bp = Blueprint('view_user')

@bp.route("/")
async def main(request):
    return json({"hello":"main"})

@bp.route("/adduser" , methods=["POST"])
async def adduser(request):
    print(request.json['username']) 
    result =insertUser({"username":request.json['username'] , "password":request.json["password"] , "email":request.json["email"]})
    if result == 0:
        return text("done")
    else:
        return text("faild")
