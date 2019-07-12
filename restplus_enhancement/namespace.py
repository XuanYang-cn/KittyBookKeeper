import logging
import six
from functools import wraps
from inspect import isfunction
from flask import g
from flask_restplus import Namespace, reqparse
from flask_restplus.reqparse import ParseResult
# from tanka.contrib.api_params import account_auth_optional_header_param
from restplus_enhancement.request_result import EnhancedParseResult
from restplus_enhancement.mixins import RequestMixin
from restplus_enhancement.schema_model import SerializationModel, fast_factory, schema_factory

logger = logging.getLogger(__name__)

class EnhancedNamespace(Namespace, RequestMixin):
    def new_schema(self, fields, name=None, model_class=SerializationModel):
        if name:
            return schema_factory(self, name, fields, model_class)
        return fast_factory(self, fields, model_class)

    def route(self, *urls, **kwargs):
        def wrapper(cls):
            # cls = default.doc(params=account_auth_optional_header_param)(cls)
            # cls = default.param('Platform', _in='header')(cls)
            doc = kwargs.pop('doc', None)
            if doc is not None:
                self._handle_api_doc(cls, doc)
            self.add_resource(cls, *urls, **kwargs)
            return cls
        return wrapper

    def response(self, code, description, model=None, validate=True, **kwargs):
        if model and isinstance(model, SerializationModel):
            as_list = kwargs.get('as_list', False)
            model = model.as_list_response if as_list else model.as_response
        if model and validate:
            return self.marshal_with(model, code=code, description=description, **kwargs)

        return super(EnhancedNamespace, self).response(code, description, model, **kwargs)

    def need_handle_expect(self, target, **kwargs):
        if not isfunction(target):
            return ''
        return self.get_expect_type(**kwargs)

    def get_expect_type(self, **kwargs):
        expect = kwargs.get('expect')
        if not expect:
            return ''

        for param in expect:
            if isinstance(param, reqparse.RequestParser):
                return 'parser'

        return 'schema'

    def doc(self, shortcut=None, **kwargs):
        '''A decorator to add some api documentation to the decorated object'''
        if isinstance(shortcut, six.text_type):
            kwargs['id'] = shortcut
        show = shortcut if isinstance(shortcut, bool) else True


        def wrapper(documented):
            self._handle_api_doc(documented, kwargs if show else False)

            def inner(func, **config):
                parsers, schemas = [], []
                expect_type = config.pop('expect_type')
                if expect_type == 'parser':
                    parsers = config.get('expect', [])
                else:
                    schemas = config.get('expect', [])

                skip_none = config.get('skip_none', False)

                @wraps(documented)
                def inner_inner(*args, **kwargs):
                    g.json_input_data = None
                    for schema in schemas:
                        logger.debug('expect_schema={}'.format(schema))
                        if not g.json_input_data:
                            g.json_input_data = self.get_json_input_or_abort(model=schema, skip_none=True)
                        else:
                            g.json_input_data = self.get_json_input_or_abort(data=g.json_input_data, model=schema, skip_none=True)

                    g.args = EnhancedParseResult()
                    for parser in parsers:
                        tmp = EnhancedParseResult()
                        p_args = parser.parse_args()
                        tmp.update(p_args)
                        tmp.build()
                        g.args.update(tmp)
                        g.args.pop('sub_result_handlers')
                        if skip_none:
                            g.args = ParseResult({k:v for k, v in g.args.items() if v is not None})

                    return func(*args, **kwargs)
                return inner_inner

            expect_type = self.need_handle_expect(documented, **kwargs)
            if expect_type:
                ret = inner(documented, expect_type=expect_type, **kwargs)
                return ret
            return documented
        return wrapper

Namespace = EnhancedNamespace