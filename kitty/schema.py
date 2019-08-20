import logging
from flask_restplus import fields
from kitty import kitty_api as api
from flask_restplus import reqparse

logger = logging.getLogger(__name__)


def paginate_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('offset', type=int, required=False, default=0,
                        location='args', help='页数')
    parser.add_argument('limit', type=int, required=False, default=10,
                        location='args', help='每页返回的数量')
    return parser


EmptySchema = api.new_schema(name='EmptySchema', fields={})

GetCategoryResponseSchema = api.new_schema(name='GetCategoryResponseSchema', fields={
    'name': fields.String(example='income', description='收入')
    })

CategoryRequestSchema = api.new_schema(name='CategoryRequestSchema', fields={
    'name': fields.String(example='income', required=True)
    })

CastegoryResponseSchema = api.new_schema(name='CastegoryResponseSchema', fields={
    'category': fields.List(fields.String(example='income'))
    })

AddTransactionRequestSchema = api.new_schema(name='AddNewTransactionSchema', fields={
    'year': fields.Integer(example=2019, description='Year when the transaction happend, default to this year', required=False),
    'month': fields.Integer(example=12, description='Month when the transaction happend, default to this month', required=False),
    'day': fields.Integer(example=1, description='Day when the transaction happend, default to today', required=False),
    'expense': fields.String(example='123.50', description='Money of this transaction', required=True),
    'category': fields.String(example='income', description='Classification of this transaction', required=True),
    'description': fields.String(example='Salary', description='Brief description about this transaction', required=True)
    })
