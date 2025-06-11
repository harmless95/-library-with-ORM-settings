from app import app
from flask_restful import Api, Resource
from flasgger import APISpec

api = Api(app)

spec = APISpec(
    title="School library",
    version="6.8.1",
    openapi_version="2.0"
)

class BookList(Resource):
    pass

class BookId(Resource):
    pass

class AuthorsList(Resource):
    pass

class AuthorId(Resource):
    pass

class StudentsList(Resource):
    pass

class StudentId(Resource):
    pass
