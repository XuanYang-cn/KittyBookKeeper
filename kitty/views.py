from flask import g
from kitty import kitty_api as api
from kitty.models import Classification, Transaction
from flask_restplus import Resource
from kitty.schema import (
        EmptySchema,
        GetCategoryResponseSchema,
        CategoryRequestSchema,
        CastegoryResponseSchema,
        AddTransactionRequestSchema,
        paginate_parser,
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

    @api.expect(paginate_parser(), validate=True)
    @api.response(200, 'sucess', CastegoryResponseSchema, validate=True)
    @api.response(400, 'fail', EmptySchema, validate=False)
    def get(self):
        """Get categorys"""
        gorys = Classification.query.page().all()
        logger.error(gorys)
        return SchemaResponse(result={
            'category': gorys
            })


@api.route('/transaction')
class TransactionRoute(Resource):
    @api.expect(AddTransactionRequestSchema)
    @api.response(200, 'success', EmptySchema, validate=True)
    @api.response(400, 'fail', EmptySchema, validate=False)
    def post(self):
        Transaction.new(**g.json_input_data)
        return SchemaResponse()
