import jwt
from .config import secrect_key

def buildToken(username):
    return jwt.encode({'sub':username},secrect_key , algorithm='HS256').decode('utf-8') 

