#each new user must have these attributes
required_data = [ 'first', 'last', 'username' ]
required_data.sort()

#error and success templates for uniform responses
#api syntax:
#missing attr values will be null.
#always return data as items in the results list, even if it is a single item.
#error messages will contain no results list
#error objects will be returned on all responses so they can be used for sanity checks.
#empty results lists will be returned when there is no useful data to retrun.
#changes will be reflected by returning the new/changed object.

errmsg = {
        "error": {
        "description": "Unspecified Failure",
        "http_code": "",
        "error_code": "",
        "reference": ""
        }
        }
successmsg = {
                "error": "null",
                "results": []
             }

#fill in the error template
def die(error, hc="null", ec="null", reference="null"):
    msg = errmsg
    msg["error"]["description"] = error
    msg["error"]["http_code"] = hc
    msg["error"]["error_code"] = ec
    msg["error"]["reference"] = reference
    return msg

#fill in the success template
def suc(data):
    msg = successmsg
    #reuse
    del msg["results"][:]
    #allow returning empty response documents for things like DELETE
    if data:
        for d in data:
            msg["results"].append(d)
    return msg

def get_all_users(d):
    l = list(map(lambda u: u['username'], d))
    return l

def get_all_keys(d):
    l = list(d.keys())
    l.sort()
    return l

def get_all_values(d):
    l = list(d.values())
    l.sort()
    return l

#find the index of the first dictionary in the list of dicts that has username = $value
def user_loc(d, match, value):
    l = next((i for i, item in enumerate(d) if item[match] == value), None)
    return l
