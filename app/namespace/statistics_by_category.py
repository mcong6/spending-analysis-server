from datetime import datetime
from http import HTTPStatus

import pandas as pd
from flask import make_response, jsonify, request
from flask_restx import Resource, Namespace

from db.models.models import TransactionModel
from utils.db_connection import DBSession

statistics_by_category_api = Namespace(name="StatisticsByCategory",
                                       path="/",
                                       description="StatisticsByCategory")


class StatisticsByCategory(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        start_date = request.args.get("startDate", "")
        end_date = request.args.get("endDate", "")
        category = request.args.get("category", "")
        trans_records = session.query(TransactionModel)
        if start_date != "":
            trans_records = trans_records.filter(
                TransactionModel.transaction_date > datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date != "":
            trans_records = trans_records.filter(
                TransactionModel.transaction_date < datetime.strptime(end_date, '%Y-%m-%d'))
        if category != "":
            trans_records = TransactionModel.filter_by(category_level2=category)

        trans_records = trans_records.all()
        if len(trans_records) == 0:
            return make_response([])
        trans_json = [i.serialize for i in trans_records]

        trans_df = pd.DataFrame(trans_json)
        trans_df = trans_df[trans_df.type == "Sale"]

        expense_by_category = trans_df.loc[:, ["amount", "category_level2"]].groupby("category_level2",
                                                                                     as_index=False).sum()
        resp = {"total": trans_df.amount.sum(),
                "count": trans_df.amount.count(),
                "max": trans_df.amount.max(),
                "min": trans_df.amount.min(),
                "query": request.args.to_dict(),
                "data": []}
        for idx, row in expense_by_category.iterrows():
            ele = {"category": row.category_level2,
                   "amount": row.amount}
            resp["data"].append(ele)
        return make_response(jsonify(resp), HTTPStatus.OK)
