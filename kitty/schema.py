import logging
from flask_restplus import fields
from kitty import kitty_api as api
from flask_restplus import reqparse

logger = logging.getLogger(__name__)


EmptySchema = api.new_schema(name='EmptySchema', fields={})

GetCategoryResponseSchema = api.new_schema(name='GetCategoryResponseSchema', fields={
    'name': fields.String(example='income', description='收入')
    })

CategoryRequestSchema = api.new_schema(name='CategoryRequestSchema', fields={
    'name': fields.String(example='income', required=True)
    })
