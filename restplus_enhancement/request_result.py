import logging
from flask_restplus.reqparse import ParseResult, RequestParser
from restplus_enhancement import exceptions

logger = logging.getLogger(__name__)

class ArgumentResult:
    @classmethod
    def build(cls, request_result):
        kwargs = {}
        for key in cls.arguments:
            value = request_result.get(key, None)
            if value is None:
                return None
            value = cls._handle_value(value)
            kwargs[key] = value

        return cls(**kwargs)

    @classmethod
    def _handle_value(cls, value):
        return value

class PagenationResult(ArgumentResult):
    arguments = ['page', 'per_page']
    def __init__(self, page, per_page):
        assert isinstance(page, int)
        assert isinstance(per_page, int)

        if page < 1:
            raise exceptions.ParseResultException('page is less than 1')
        if per_page > 50 or per_page < 1:
            raise exceptions.ParseResultException('per_page is not between [1,50]')
        self.page = page
        self.per_page = per_page

    @property
    def start(self):
        return self.per_page*(self.page-1)

    @property
    def end(self):
        return self.start + self.per_page

class JsonServerPagenationResult(ArgumentResult):
    arguments = ['offset', 'pagesize']
    def __init__(self, offset, pagesize):
        assert isinstance(offset, int)
        assert isinstance(pagesize, int)
        self.offset = offset
        self.pagesize = pagesize

    @property
    def start(self):
        return None if self.offset < 0 else self.offset

    @property
    def end(self):
        return None if self.offset < 0 else (self.offset + self.pagesize)

class SiblingsResult(ArgumentResult):
    arguments = ['_sibling']
    def __init__(self, _sibling):
        self.siblings = _sibling

    @classmethod
    def _handle_value(cls, value):
          return [x.strip() for x in value.split(',')]

    def joined(self, other):
        return [x for x in self.siblings if x in other]

class ExpandResult(ArgumentResult):
    arguments = ['expand']
    def __init__(self, expand):
        self.expand = expand

    @classmethod
    def _handle_value(cls, value):
        return [x.strip() for x in value.split(',')]

    def joined(self, other):
        return [x for x in self.expand if x in other]

class PageMixin:
    def __init__(self):
        self.sub_result_handlers.update(pagenation=PagenationResult)
        self.pagenation = None
        super(PageMixin, self).__init__()

class JSPageMixin:
    def __init__(self):
        self.sub_result_handlers.update(jspagenation=JsonServerPagenationResult)
        self.jspagenation = None
        super(JSPageMixin, self).__init__()

class SiblingMixin:
    def __init__(self):
        self.sub_result_handlers.update(siblings=SiblingsResult)
        self.siblings = None
        super(SiblingMixin, self).__init__()

class ExpandMixin:
    def __init__(self):
        self.sub_result_handlers.update(expand=ExpandResult)
        self.expand = None
        super(ExpandMixin, self).__init__()

class EnhancedParseResult(ExpandMixin, SiblingMixin, PageMixin, JSPageMixin, ParseResult):
    def __init__(self):
        self.sub_result_handlers = {}
        super(EnhancedParseResult, self).__init__()

    def build(self):
        for name, sub_class in self.sub_result_handlers.items():
            instance = sub_class.build(self)

            if not instance:
                continue
            setattr(self, name, instance)

    @property
    def start(self):
        if self.jspagenation and self.jspagenation.start is not None:
            return self.jspagenation.start
        elif self.pagenation and self.pagenation.start is not None:
            return self.pagenation.start

        return None

    @property
    def end(self):
        if self.jspagenation and self.jspagenation.end is not None:
            return self.jspagenation.end
        elif self.pagenation and self.pagenation.end is not None:
            return self.pagenation.end

        return None

class EnhancedRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        kwargs.pop('result_class', None)
        super(EnhancedRequestParser, self).__init__(*args, result_class=EnhancedParseResult, **kwargs)
