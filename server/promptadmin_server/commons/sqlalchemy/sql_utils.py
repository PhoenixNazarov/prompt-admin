from sqlmodel import SQLModel, select
from ..dto.view_params_comparison import ComparisonType


class SqlUtils:
    @staticmethod
    def unpack(rows):
        return [i[0] for i in rows]

    @staticmethod
    def build_statement_by_view_params(model: type(SQLModel), view_params):
        statement = select(model)
        for f in view_params.filters:
            if isinstance(f.value, list):
                statement = statement.where(f.field.in_(f.value))
            else:
                if f.like:
                    statement = statement.where(f.field.like(f.value))
                else:
                    statement = statement.where(f.field == f.value)

        for c in view_params.comparisons:
            if c.comparison == ComparisonType.LT:
                statement = statement.where(c.field < c.value)
            elif c.comparison == ComparisonType.LE:
                statement = statement.where(c.field <= c.value)
            elif c.comparison == ComparisonType.EQ:
                statement = statement.where(c.field == c.value)
            elif c.comparison == ComparisonType.NE:
                statement = statement.where(c.field != c.value)
            elif c.comparison == ComparisonType.GT:
                statement = statement.where(c.field > c.value)
            elif c.comparison == ComparisonType.GE:
                statement = statement.where(c.field >= c.value)

        for o in view_params.orders:
            if o.desc:
                statement = statement.order_by(o.field.desc())
            else:
                statement = statement.order_by(o.field.asc())

        if view_params.count:
            statement = statement.limit(view_params.count)

        if view_params.page:
            statement = statement.offset(view_params.count * view_params.page)

        return statement

    @staticmethod
    def build_filter(model, field, value):
        statement = select(model)
        if isinstance(value, list):
            statement = statement.where(field.in_(value))
        else:
            statement = statement.where(field == value)
        return statement
