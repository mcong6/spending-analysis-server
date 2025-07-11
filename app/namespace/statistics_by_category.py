from datetime import datetime
from http import HTTPStatus

import pandas as pd
from flask import make_response, jsonify, request
from flask_restx import Resource, Namespace

from app.db.models.models import TransactionModel
from app.utils.db_connection import DBSession

statistics_by_category_api = Namespace(name="StatisticsByCategory",
                                       path="/",
                                       description="Operations related to spending statistics by category")


class StatisticsByCategory(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        """Retrieves spending statistics grouped by category.

        Query Parameters:
            startDate (str, optional): Start date for filtering transactions (YYYY-MM-DD).
            endDate (str, optional): End date for filtering transactions (YYYY-MM-DD).
            category (str, optional): Filter by a specific category level 2.

        Returns:
            JSON: A dictionary containing total amount, count, max/min amount, query parameters, and a list of category-wise spending.
        """
        start_date = request.args.get("startDate", "")
        end_date = request.args.get("endDate", "")
        category = request.args.get("category", "")
        trans_records = session.query(TransactionModel).filter(TransactionModel.type_name == "Sale")
        if start_date != "":
            trans_records = trans_records.filter(
                TransactionModel.transaction_date > datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date != "":
            trans_records = trans_records.filter(
                TransactionModel.transaction_date < datetime.strptime(end_date, '%Y-%m-%d'))
        if category != "":
            trans_records = trans_records.filter(TransactionModel.category_level2 == category)

        trans_records = trans_records.all()
        if len(trans_records) == 0:
            return make_response([])
        trans_json = [i.serialize for i in trans_records]

        trans_df = pd.DataFrame(trans_json)

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
