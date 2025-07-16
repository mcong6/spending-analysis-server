import logging
from datetime import datetime

from app.constant.system_constants import SYSTEM_USER_NAME
from app.db.models.models import TransactionModel

logger = logging.getLogger(__name__)


def add_transaction(session, transaction_data):
    """
    Creates a new transaction record from the given data and adds it to the session.
    It sanitizes foreign key fields by converting empty strings to None.
    """
    # Sanitize foreign key fields to ensure empty strings become NULL in the database
    category_level1 = transaction_data.get('category_level1') or None
    category_level2 = transaction_data.get('category_level2') or None
    type_name = transaction_data.get('type_name') or None
    source = transaction_data.get('source') or None

    # Create the new transaction
    logger.info(f"Adding transaction to session: {transaction_data.get('description')}")
    new_trans = TransactionModel(
        transaction_date=datetime.strptime(transaction_data['transaction_date'], '%m/%d/%Y'),
        description=transaction_data.get('description'),
        notes=transaction_data.get('notes'),
        category_level1=category_level1,
        category_level2=category_level2,
        type_name=type_name,
        amount=transaction_data.get('amount'),
        source=source,
        created_at=datetime.now(),
        created_by=SYSTEM_USER_NAME,
        modified_at=datetime.now(),
        modified_by=SYSTEM_USER_NAME
    )
    session.add(new_trans)