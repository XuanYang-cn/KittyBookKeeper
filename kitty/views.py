from flask import g
from kitty import kitty_api as api
from kitty.models import Classification
from flask_restplus import Resource
from kitty.schema import (
        EmptySchema,
        GetCategoryResponseSchema,
        CategoryRequestSchema,
)
from restplus_enhancement.schema_model import SchemaResponse
import logging
logger = logging.getLogger(__name__)

@api.route('/category')
class Category(Resource):
    @api.expect(CategoryRequestSchema)
    @api.response(200, 'success', GetCategoryResponseSchema, validate=True)
    @api.response(400, 'fail', EmptySchema, validate=False)
    def post(self):
        """Add new category """
        new_category = Classification()
        new_category.new(**g.json_input_data)
        return SchemaResponse(new_category)
