import falcon
from .users import Users

api = application = falcon.API()

users = Users()
api.add_route('/v1/users/{username}', users)
api.add_route('/v1/users', users)
