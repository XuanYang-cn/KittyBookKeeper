import enum
from sqlalchemy import inspect
from sqlalchemy.orm.properties import RelationshipProperty, ColumnProperty
from kitty import db


class SerializationMixin:
    @property
    def as_response(self):
        return self

    def to_dict(self, exclude=['ids'], extra=None):
        insp = inspect(self.__class__)

        columns = []

        for attr in insp.attrs:
            if attr.key.startswith('__'):
                continue
            if not isinstance(attr, ColumnProperty):
                continue
            columns.append(attr.key)

        for x in exclude:
            columns.remove(x)

        return_dict = {}
        for y in columns:
            return_dict[y] = getattr(self, y)

        if extra:
            return_dict.update(extra)

        return return_dict


class CRUDMixin:
    def commit(self):
        db.session.commit()

    def save(self):
        if self.id is None:
            db.session.add(self)
        return self.commit()

    def diacard(self, commit=True):
        self.status = self.DISCARDED
        if not commit:
            return self
        return self.commit

    def delete(self):
        db.session.delete(self)
        return self.commit()

    def is_kept(self):
        return self.status == self.KEPT

    def is_discarded(self):
        return self.status == self.DISCARDED


class BaseModel(db.Model, CRUDMixin, SerializationMixin):
    __abstract__ = True
    KEPT = 0
    DISCARDED = 1

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_on = db.Column(db.DateTime, nullable=False, default=db.func.now(),
                           onupdate=db.func.now())
    status = db.Column(db.Integer, default=0)  # Status of current record, 0 is normal


class FileBaseModel(db.Model, CRUDMixin, SerializationMixin):
    __abstract__ = True
    KEPT = 0
    DISCARDED = 1

    id = db.Column(db.Integer, primary_key=True)
    upload_on = db.Column(db.DateTime, nullable=False, default=db.func.now())


class SimpleModel(db.Model, CRUDMixin, SerializationMixin):
    __abstract__ = True


class ModelEnum(enum.Enum):
    @classmethod
    def members(cls):
        return cls._member_names_
