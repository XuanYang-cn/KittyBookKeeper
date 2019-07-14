import logging
import datetime

from kitty import db, settings
from kitty.base import BaseModel

logger = logging.getLogger(__name__)


class Classification(BaseModel):

    __tablename__ = 'transaction_classification'

    name = db.Column(db.String(20), nullable=False, unique=True)


class Transaction(BaseModel):

    __tablename__ = 'transaction'

    expense = db.Column(db.Numeric(10, 2), nullable=False)
    classification_id = db.Column(db.Integer, nullable=False, index=True)

    classification = db.relationship(
        Classification,
        primaryjoin='and_(foreign(Transaction.classification_id) == Classification.id,\
                            Classification.status == 0)'
    )
