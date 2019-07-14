from flask_restplus import fields
from kitty import kitty_api as api


EmptySchema = api.new_schema(name='EmptySchema', fields={})
