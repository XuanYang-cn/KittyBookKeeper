import logging
import datetime
from decimal import Decimal

from kitty import db, settings
from kitty.base import BaseModel
from kitty.errors import (
    CategoryAlreadyExistsError,
    CategoryNotExistsError,
)

logger = logging.getLogger(__name__)


class Classification(BaseModel):

    __tablename__ = 'transaction_classification'

    name = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f"<Classification: {self.name}>"

    def __str__(self):
        return f"{self.name}"

    def new(self, name):
        item = Classification.query.filter_by(name=name).first()

        if item:
            raise CategoryAlreadyExistsError('Category already existed!')

        self.name = name
        self.save()


def parse_date(year=None, month=None, day=None):
    # TODO test
    # TODO may raisee Exceptions
    today = datetime.date.today()
    expense_year = year or today.year
    expense_month = month or today.month
    expense_day = day or today.day

    return datetime.date(expense_year, expense_month, expense_day)


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

    def __repr__(self):
        return f"<Transaction: expense:{self.expense} date: {self.spend_on}>"

    @classmethod
    def new(cls, category, expense, description, *, year=None, month=None, day=None):
        '''
        expense: str
        '''
        spend_on = parse_date(year, month, day)
        category = Classification.query.filter_by(name=category).first()
        expense = Decimal(expense)

        if category:
            trans = Transaction(expense=expense, classification=category,
                                spend_on=spend_on, description=description)
            trans.save()
        else:
            raise CategoryNotExistsError('Category not exists!')
