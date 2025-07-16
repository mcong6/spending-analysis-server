from app.extension import db


class DBSession:
    @staticmethod
    def func(func):
        def inner_func(*args, **kwargs):
            session = db.session()
            try:
                res = func(session, *args, **kwargs)
                session.commit()
            except Exception:
                session.rollback()
                raise
            return res

        return inner_func

    @staticmethod
    def class_method(func):
        def inner_func(self, *args, **kwargs):
            session = db.session()
            try:
                res = func(self, session, *args, **kwargs)
                session.commit()
            except Exception:
                session.rollback()
                raise
            return res

        return inner_func