from datetime import datetime
from http import HTTPStatus

import pandas as pd
from flask import make_response, jsonify, request
from flask_restx import Resource, Namespace

from db.models.models import TransactionModel
from utils.db_connection import DBSession

statistics_by_source_api = Namespace(name="StatisticsBySource",
                                     path="/",
                                     description="StatisticsBySource")


class StatisticsBySource(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        start_date = request.args.get("startDate", "")
        end_date = request.args.get("endDate", "")
        trans_records = session.query(TransactionModel)
        if start_date != "":
            trans_records = trans_records.filter(
                TransactionModel.transaction_date > datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date != "":
            trans_records = trans_records.filter(
                TransactionModel.transaction_date < datetime.strptime(end_date, '%Y-%m-%d'))

        trans_records = trans_records.all()
        trans_json = [i.serialize for i in trans_records]

        trans_df = pd.DataFrame(trans_json)
        trans_df = trans_df[trans_df.type == "Sale"]

        expense_by_category = trans_df.loc[:, ["amount", "source"]].groupby("source",
                                                                            as_index=False).sum()
        resp = {"total": trans_df.amount.sum(),
                "count": trans_df.amount.count(),
                "max": trans_df.amount.max(),
                "min": trans_df.amount.min(),
                "query": request.args.to_dict(),
                "data": []}
        for idx, row in expense_by_category.iterrows():
            ele = {"source": row.source,
                   "amount": row.amount}
            resp["data"].append(ele)
        return make_response(jsonify(resp), HTTPStatus.OK)
