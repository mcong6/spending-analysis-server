from app.namespace.index import index_api
from app.namespace.statistics_by_category import statistics_by_category_api
from app.namespace.statistics_by_date import statistics_by_date_api
from app.namespace.statistics_by_source import statistics_by_source_api
from app.namespace.trans_category import transaction_category_api
from app.namespace.trans_source import transaction_source_api
from app.namespace.trans_type import transaction_type_api
from app.namespace.transactions import transaction_api


def init_api(api):
    api.add_namespace(index_api)
    api.add_namespace(transaction_api)
    api.add_namespace(transaction_category_api)
    api.add_namespace(transaction_type_api)
    api.add_namespace(transaction_source_api)
    api.add_namespace(statistics_by_category_api)
    api.add_namespace(statistics_by_date_api)
    api.add_namespace(statistics_by_source_api)