import logging
import uuid
from flask import g
from flask_restplus import marshal, Model, fields
from restplus_enhancement import exceptions

logger = logging.getLogger(__name__)


def response_schema(api, result_schema, name=None, as_list=False, envolope='list'):
    if not name:
        list_flag = 'List' if as_list else ''
        schema_name = result_schema.name[1:] if result_schema.name.startswith('_') else result_schema.name
        name = schema_name + list_flag + 'Response'
    if not as_list:
        return api.model(name, {
            'code': fields.Integer,
            'message': fields.String,
            'result': fields.Nested(result_schema)
        })
    list_result_schema = api.model('_'+name, {
        envolope: fields.List(fields.Nested(result_schema), default=[])
    })
    # logger.info(name)

    return response_schema(api, list_result_schema, name=name, as_list=False)


class SerializationModel(Model):
    def add_api(self, api):
        self.api = api
        self.response_list_schema = None
        self.response_schema = None

    def serialize(self, data, **kwargs):
        super(SerializationModel, self).validate(data)
        self.check_payload(data, **kwargs)
        self.validated_data = data
        self.check(data, **kwargs)

    def check(self, data, **kwargs):
        pass

    def check_payload(self, data, **kwargs):
        for k, v in kwargs.items():
            if v is not True:
                continue
            if k not in data:
                raise exceptions.InputPayloadValidationFail('\"{}\" is needed'.format(k))

    def save(self, **kwargs):
        return self.create(**kwargs)

    def create(self, **kwargs):
        return {}

    @property
    def as_response(self):
        if self.response_schema:
            return self.response_schema

        self.response_schema = response_schema(self.api, self)

        return self.response_schema

    @property
    def as_list_response(self):
        if self.response_list_schema:
            return self.response_list_schema

        self.response_list_schema = response_schema(self.api, self, None, True)
        return self.response_list_schema


def schema_marshal(data, fields, **kwargs):
    if isinstance(fields, SerializationModel):
        fields.serialize(data, **kwargs)
        return fields.validated_data

    return marshal(data, fields, **kwargs)


def schema_marshal_args(fields, **kwargs):
    data = g.args
    # data.pop('sub_result_handlers')
    return schema_marshal(data, fields, **kwargs)


class DictMixin(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class SchemaResponse(DictMixin):
    def __init__(self, result={}, code=0, message='', as_list=False, errors=None, evelope='list'):
        if evelope and as_list:
            self.result = {
                evelope: result
            }
        else:
            self.result = result
        self.code = code
        self.message = message
        if errors: self.result = errors

    @property
    def data(self):
        return {
            'result': self.result,
            'code': self.code,
            'message': self.message
        }


class SchemaListResponse:
    def __init__(self, result={}, code=0, message=''):
        self.result = {
            'list': result
        }
        self.code = code
        self.message = message


def schema_factory(api, name, fields, model_class=SerializationModel):
    model = model_class(name, fields)
    model = api.add_model(model.name, model)
    if issubclass(model_class, SerializationModel):
        model.add_api(api)
    return model


def fast_factory(api, fields, model_class=SerializationModel):
    name = str(uuid.uuid4())
    return schema_factory(api, name, fields, model_class)


def response_schema_factory(api, name, fields, as_list=False, evelope='list', model_class=SerializationModel):
    if isinstance(fields, Model):
        model = fields
    else:
        model = schema_factory(api, name, fields, model_class)
    if issubclass(model_class, SerializationModel):
        return model.as_response
    return response_schema(api, model, None, as_list, evelope)
