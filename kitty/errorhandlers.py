from kitty import kitty_api as api
from kitty.errors import (
        CategoryAlreadyExistsError,
        )
from restplus_enhancement.schema_model import SchemaResponse
from flask_restplus.model import HTTPStatus


@api.errorhandler(CategoryAlreadyExistsError)
def CategoryAlreadyExistsErrorHandler(error):
    return SchemaResponse(code=error.code,
                          message=str(error),
                          ), HTTPStatus.BAD_REQUEST
