from flask_restful import Api, Resource
import flask
from tinydb import TinyDB, Query
import get_data

db = TinyDB('data.json')
get_data.get_data(db)
table=db.table('_default', cache_size=None)


## DB lookup
def get_country_name(code) :
    db = TinyDB('data.json')
    country = Query()
    doc = db.get(country['code'] == code)
    return doc


def get_country_code(name) :
    db = TinyDB('data.json')
    country = Query()
    doc = db.get(country['name'] == name)
    return doc


## Flask API

app = flask.Flask(__name__)
api = Api(app)


class CountryCode(Resource) :
    def get(self, name) :
        doc = get_country_code(name)
        if doc ==None:
           response='No Data Found'
        else:
           response=doc['code']
        return { name : response}


class CountryName(Resource) :
    def get(self, code) :
        doc = get_country_name(code)
        if doc ==None:
           response="No Data Found"
        else:
           response=doc['name']
        return { code : response }


class Health(Resource) :
    def get(self) :
        response = get_country_code('India')['code']
        if response == 'IN' :
            return {'status' : 'OK'}
        else :
            return {'status' : 'FAILED'}


class Diag(Resource) :
    def get(self) :
        res = get_data.dataApiStatus()
        if res.status_code == 200 :
            return {"api_status" : 200, "status" : "ok"}
        else :
            return {"api_status" : res, "status" : "failed"}


api.add_resource(Health, "/health")
api.add_resource(Diag, "/diag")
api.add_resource(CountryCode, "/convert/<string:name>")
api.add_resource(CountryName, "/convert_name/<string:code>")

if __name__ == '__main__' :
    app.run(host="0.0.0.0")
