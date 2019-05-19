import json
import falcon
from .lib import *
from .data import *

#/users endpoint
class Users(object):
    #display all the users
    def on_get(self, req, resp, username=None):
        if len(req.path.split('/')) == 3:
            while True:
                try:
                    msg = suc(data["users"])
                    resp.status = falcon.HTTP_200
                    break
                except:
                    msg = die(error="unable to get user list", hc=500)
                    resp.status = falcon.HTTP_500
                    break
        else:
        #display a single user in results list
            while True:
                try:
                    requsername = req.path.split('/')[3]
                    location = user_loc(data['users'], 'username', requsername)
                except:
                    msg = die(error="user lookup failed", hc=500)
                    resp.status = falcon.HTTP_500
                    break
                if location != None:
                    tl = []
                    tl.append(data['users'][location])
                    msg = suc(tl)
                    resp.status = falcon.HTTP_200
                    break
                else:
                    msg = die(error="user not found", hc=404)
                    resp.status = falcon.HTTP_404
                    break
        resp.body = json.dumps(msg, ensure_ascii=False)

    #add a new user. return the user in the results list
    def on_post(self, req, resp, username=None):
        while True:
            #dont add existing users
            try:
                existing_users = get_all_users(data['users'])
            except:
                msg = die(error="unable to get all users", hc=500)
                resp.status = falcon.HTTP_500
                break
            if req.media["username"] in existing_users:
                msg = die(error="user with that username already exists", hc=409)
                resp.status = falcon.HTTP_409
                break
            #must add all data with the user
            try:
                rs = get_all_keys(req.media)
            except:
                msg = die(error="input data is malformed", hc=400)
                resp.status = falcon.HTTP_400
                break
            if required_data != rs:
                msg = die(error="you must specify all attributes of the user you are adding", hc=400)
                resp.status = falcon.HTTP_400
                break
            #data added cannot be null
            try:
                rs = get_all_values(req.media)
            except:
                msg = die(error="input data is malformed", hc=400)
                resp.status = falcon.HTTP_400
                break
            if not all(rs):
                msg = die(error="values for the new user must not be null", hc=422)
                resp.status = falcon.HTTP_422
                break
            #add the user
            try:
                data['users'].append(req.media)
            except:
                msg = die(error="unable to add the user", hc=500)
                resp.status = falcon.HTTP_500
                break
            else:
                location = user_loc(data['users'], 'username', req.media['username'])
                tl = []
                tl.append(data['users'][location])
                msg = suc(tl)
                resp.status = falcon.HTTP_201
                break
        resp.body = json.dumps(msg, ensure_ascii=False)

    #delete a user then return an empty results list and 200
    def on_delete(self, req, resp, username):
        while True:
            try:
                requsername = req.path.split('/')[3]
                location = user_loc(data['users'], 'username', requsername)
            except:
                msg = die(error="user lookup failed", hc=500)
                resp.status = falcon.HTTP_500
                break
            if location != None:
                del data['users'][location]
                msg = suc(None)
                resp.status = falcon.HTTP_200
                break
            else:
                msg = die(error="user not found", hc=404)
                resp.status = falcon.HTTP_404
                break
        resp.body = json.dumps(msg, ensure_ascii=False)

    #update the attributes of a user then display that user in the results list
    def on_patch(self, req, resp, username):
        while True:
            try:
                requsername = req.path.split('/')[3]
                location = user_loc(data['users'], 'username', requsername)
            except:
                msg = die(error="user lookup failed", hc=500)
                resp.status = falcon.HTTP_500
                break
            try:
                rs = get_all_keys(req.media)
            except:
                msg = die(error="input data is malformed", hc=400)
                resp.status = falcon.HTTP_400
                break
            for k,v in req.media.iteritems():
                if k in required_data and k != "username":
                    data['users'][location][k] = v
            tl = []
            tl.append(data['users'][location])
            msg = suc(tl)
            resp.status = falcon.HTTP_200
            break
        resp.body = json.dumps(msg, ensure_ascii=False)
