from extension import db
from lib.datetime_utils import dump_date, dump_datetime


class TransactionCategoryModel(db.Model):
    __tablename__ = 'category'
    __table_args__ = {"schema": "public"}
    category = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)


class TransactionSourceModel(db.Model):
    __tablename__ = 'source'
    __table_args__ = {"schema": "public"}
    source = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)


class TransactionTypeModel(db.Model):
    __tablename__ = 'type'
    __table_args__ = {"schema": "public"}
    type = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)


class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {"schema": "public"}
    transaction_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    transaction_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    category_level1 = db.Column(db.String(50), nullable=False)
    category_level2 = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'transaction_id': self.transaction_id,
            'transaction_date': dump_date(self.transaction_date),
            'description': self.description,
            'notes': self.notes,
            'category_level1': self.category_level1,
            'category_level2': self.category_level2,
            'type': self.type,
            'amount': self.amount,
            'source': self.source,
            'created_at': dump_datetime(self.created_at),
            'created_by': self.created_by,
            'modified_at': dump_datetime(self.modified_at),
            'modified_by': self.modified_by
        }
