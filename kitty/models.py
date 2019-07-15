import logging
import datetime

from kitty import db, settings
from kitty.base import BaseModel
from kitty.errors import CategoryAlreadyExistsError

logger = logging.getLogger(__name__)


class Classification(BaseModel):

    __tablename__ = 'transaction_classification'

    name = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f"<Classification: {self.name}>"

    def new(self, name):
        item = Classification.query.filter_by(name=name).first()

        if item:
            raise CategoryAlreadyExistsError('Category already existed!')

        self.name = name
        self.save()


class Transaction(BaseModel):

    __tablename__ = 'transaction'

    expense = db.Column(db.Numeric(10, 2), nullable=False)
    classification_id = db.Column(db.Integer, nullable=False, index=True)
    description = db.Column(db.String(20), nullable=False)
    spend_on = db.Column(db.Date, nullable=False)

    classification = db.relationship(
        Classification,
        primaryjoin='and_(foreign(Transaction.classification_id) == Classification.id,\
                            Classification.status == 0)'
    )
