from sanic.blueprints import Blueprint
from sanic.response import json

bp = Blueprint('view_user')


@bp.route("/")
async def main(request):
    return json({"hello":"main"})


