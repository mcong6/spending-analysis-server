from datetime import datetime
from http import HTTPStatus

import pandas as pd
from flask import make_response, jsonify, request
from flask_restx import Resource, Namespace

from db.models.models import TransactionModel
from lib.exception import ClientException
from utils.db_connection import DBSession

statistics_by_date_api = Namespace(name="StatisticsByDate",
                                   path="/",
                                   description="StatisticsByDate")


class StatisticsByDate(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        start_date = request.args.get("startDate", "")
        end_date = request.args.get("endDate", "")
        is_month = request.args.get("by", "") == "month"
        is_year = request.args.get("by", "") == "year"
        is_day = request.args.get("by", "") == "day"
        is_quarter = request.args.get("by", "") == "quarter"
        if request.args.get("by", "") == "" or request.args.get("by", "") not in ["year", "month", "day", "quarter"]:
            raise ClientException(
                f"'by' is required query parameter. It can be one of {['year', 'month', 'day', 'quarter']}.")
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
        trans_df["month"] = pd.to_datetime(trans_df['transaction_date']).dt.year.astype(str) + '-' + \
                            pd.to_datetime(trans_df['transaction_date']).dt.month.astype(str)
        trans_df["year"] = pd.DatetimeIndex(trans_df['transaction_date']).year.astype(str)
        trans_df["day"] = trans_df['transaction_date']
        trans_df["quarter"] = pd.to_datetime(trans_df['transaction_date']).dt.year.astype(str) + '-' + \
                              pd.to_datetime(trans_df['transaction_date']).dt.quarter.astype(str)+'Q'

        if is_month:
            expense_by_date = trans_df.loc[:, ["month", "amount"]].groupby("month", as_index=False).sum()
            expense_by_date = expense_by_date.sort_values('month', key=lambda x: pd.to_datetime(x))
        elif is_year:
            expense_by_date = trans_df.loc[:, ["year", "amount"]].groupby("year", as_index=False).sum()
            expense_by_date = expense_by_date.sort_values('year')
        elif is_day:
            expense_by_date = trans_df.loc[:, ["day", "amount"]].groupby("day", as_index=False).sum()
            expense_by_date = expense_by_date.sort_values('day', key=lambda x: pd.to_datetime(x))
        elif is_quarter:
            expense_by_date = trans_df.loc[:, ["quarter", "amount"]].groupby("quarter", as_index=False).sum()
            expense_by_date = expense_by_date.sort_values('quarter')
        else:
            raise Exception(
                f"Empty response. 'by' is required query parameter. It can be one of {['year', 'month', 'day', 'quarter']}.")
        resp = {"total": trans_df.amount.sum(),
                "count": trans_df.amount.count(),
                "max": trans_df.amount.max(),
                "min": trans_df.amount.min(),
                "query": request.args.to_dict(),
                "data": []}
        if is_month:
            for idx, row in expense_by_date.iterrows():
                ele = {"date": str(row.month),
                       "amount": row.amount}
                resp["data"].append(ele)
        elif is_year:
            for idx, row in expense_by_date.iterrows():
                ele = {"date": str(row.year),
                       "amount": row.amount}
                resp["data"].append(ele)
        elif is_day:
            for idx, row in expense_by_date.iterrows():
                ele = {"date": str(row.day),
                       "amount": row.amount}
                resp["data"].append(ele)
        elif is_quarter:
            for idx, row in expense_by_date.iterrows():
                ele = {"date": str(row.quarter),
                       "amount": row.amount}
                resp["data"].append(ele)

        return make_response(jsonify(resp), HTTPStatus.OK)
