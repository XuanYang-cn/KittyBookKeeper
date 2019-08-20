from flask import g
from sqlalchemy.orm import noload
from flask_sqlalchemy_caching import CachingQuery

class BaseQuery(CachingQuery):

    @property
    def kept(self):
        return self.filter_by(status=0)

    @property
    def noload(self):
        return self.options(noload('*'))

    def slice_from_args(self):
        return self.slice(g.args.start, g.args.end)

    def page(self):
        limit = g.args['limit']
        limit = 20 if limit > 20 else limit
        return self.offset(g.args['offset']).limit(limit)

    def discard(self):
        return self.update({'status': 1})
