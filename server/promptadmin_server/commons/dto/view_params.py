from typing import Optional

from pydantic import BaseModel
from .view_params_filter import ViewParamsFilter
from .view_params_order import ViewParamsOrder
from .view_params_comparison import ViewParamsComparison


class ViewParams(BaseModel):
    # Dtp for generating a query to the database

    # Set LIMIT
    count: Optional[int] = None
    # Set OFFSET = count * page
    page: Optional[int] = None

    # Set WHERE (filter-1 and filter-2 and ... filter-n)
    filters: list[ViewParamsFilter]
    # Set ORDER BY
    orders: list[ViewParamsOrder]
    # SET WHERE (comparison-1 and comparison-2 and ... comparison-n)
    comparisons: list[ViewParamsComparison]


class ViewParamsBuilder:
    def __init__(self):
        self._count = None
        self._page = None
        self.filters: list[ViewParamsFilter] = []
        self.orders: list[ViewParamsOrder] = []
        self.comparisons: list[ViewParamsComparison] = []

    def set_count(self, count: int):
        self._count = count
        return self

    def count(self, count: int):
        self._count = count
        return self

    def set_page(self, page: int):
        self._page = page
        return self

    def page(self, page: int):
        self._page = page
        return self

    def add_filter(self, _filter: ViewParamsFilter):
        self.filters.append(_filter)
        return self

    def filter(self, _filter: ViewParamsFilter):
        self.filters.append(_filter)
        return self

    def add_order(self, order: ViewParamsOrder):
        self.orders.append(order)
        return self

    def order(self, order: ViewParamsOrder):
        self.orders.append(order)
        return self

    def add_comparison(self, comparison: ViewParamsComparison):
        self.comparisons.append(comparison)
        return self

    def comparison(self, comparison: ViewParamsComparison):
        self.comparisons.append(comparison)
        return self

    def build(self) -> ViewParams:
        return ViewParams(
            count=self._count,
            page=self._page,
            filters=self.filters,
            orders=self.orders,
            comparisons=self.comparisons
        )
