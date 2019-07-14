from kitty import kitty_api as api 
from flask_restplus import Resource

@api.route('/test')
class Test(Resource):
    def get(self):
        return {'Hello': 'Tester'}
