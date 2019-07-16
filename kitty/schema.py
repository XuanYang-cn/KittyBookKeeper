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
