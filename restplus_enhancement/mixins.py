import logging
from flask import request
from flask_restplus import marshal
from restplus_enhancement import exceptions

logger = logging.getLogger(__name__)

class RequestMixin:
    def get_json_input(self):
        return request.get_json(silent=True)

    def get_json_input_or_abort(self, data=None, model=None, **kwargs):
        data = data if data else self.get_json_input()

        if data is None:
            logger.error('No json input data found')
            raise exceptions.RequestException()
        logger.info('Input json data is:{}'.format(data))
        return marshal(data, model, **kwargs) if model else data


class HandlerProxyMixin:
    def __getattr__(self, name):
        if name not in self.__dict__:
            logger.debug('Calling {}::{}'.format(self.NAME, name))
            return getattr(self.handler, name)

        return self.__dict__[name]


class ModelProxyMixin:
    def __getattr__(self, name):
        if name not in self.__dict__:
            model_attr = getattr(self.db_model, name, None)
            if model_attr is None:
                model_attr = getattr(self.model, name, None)

            return model_attr

        return self.__dict__[name]
