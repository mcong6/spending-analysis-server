from namespace.index import index_api, Index
from namespace.statistics_by_category import StatisticsByCategory, statistics_by_category_api
from namespace.statistics_by_date import statistics_by_date_api, StatisticsByDate
from namespace.statistics_by_source import statistics_by_source_api, StatisticsBySource
from namespace.trans_category import transaction_category_api, TransactionCategory
from namespace.trans_source import TransactionSource, transaction_source_api
from namespace.trans_type import transaction_type_api, TransactionType
from namespace.transactions import transaction_api, Transaction


def init_api(api):
    api.add_namespace(index_api)
    index_api.add_resource(Index, '/')
    api.add_namespace(transaction_api)
    transaction_api.add_resource(Transaction, '/transaction')
    api.add_namespace(transaction_category_api)
    transaction_category_api.add_resource(TransactionCategory, '/transaction_category')
    api.add_namespace(transaction_type_api)
    transaction_type_api.add_resource(TransactionType, '/transaction_type')
    api.add_namespace(transaction_source_api)
    transaction_source_api.add_resource(TransactionSource, '/transaction_source')
    api.add_namespace(statistics_by_category_api)
    statistics_by_category_api.add_resource(StatisticsByCategory, '/statistics_by_category')
    api.add_namespace(statistics_by_date_api)
    statistics_by_date_api.add_resource(StatisticsByDate, '/statistics_by_date')
    api.add_namespace(statistics_by_source_api)
    statistics_by_source_api.add_resource(StatisticsBySource, '/statistics_by_source')
