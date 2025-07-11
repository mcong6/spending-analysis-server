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
    type_name = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)


class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {"schema": "public"}
    transaction_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    transaction_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    category_level1 = db.Column(db.String(50), db.ForeignKey('public.category.category'), nullable=False)
    category_level2 = db.Column(db.String(50), db.ForeignKey('public.category.category'), nullable=False)
    type_name = db.Column(db.String(50), db.ForeignKey('public.type.type_name'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    source = db.Column(db.String(50), db.ForeignKey('public.source.source'), nullable=False)

    category1_rel = db.relationship('TransactionCategoryModel', foreign_keys=[category_level1], backref='transactions_level1')
    category2_rel = db.relationship('TransactionCategoryModel', foreign_keys=[category_level2], backref='transactions_level2')
    type_rel = db.relationship('TransactionTypeModel', foreign_keys=[type_name], backref='transactions')
    source_rel = db.relationship('TransactionSourceModel', foreign_keys=[source], backref='transactions')
    created_at = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<TransactionModel(transaction_id={self.transaction_id}, description='{self.description}')>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
            'type': self.type_name,
            'amount': self.amount,
            'source': self.source,
            'created_at': dump_datetime(self.created_at),
            'created_by': self.created_by,
            'modified_at': dump_datetime(self.modified_at),
            'modified_by': self.modified_by
        }
