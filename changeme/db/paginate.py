import math
from sqlalchemy.orm.query import Query
# https://github.com/wizeline/sqlalchemy-pagination


class Page:
    """
    items: The items of the current page base on the query
    total: Total number of items
    pages: Total number of pages
    has_next: Boolean indication wether there are more pages to fetch
    has_previous: Boolean indicating wether there are previous pages
    next_page: Next page number or None if the current page is the last one
    previous_page: Previous page number or None if the current page is the
    last one
    """

    def __init__(self, items, page, page_size, total):
        self.items = items
        self.prev_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.prev_page = page - 1
        prev_items = (page - 1) * page_size
        self.has_next = prev_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))


def paginate(query: Query, page: int, page_size: int) -> Page:
    """
    This function create Page object which could be use
    to iterate from results.

    Example call:
        from sqlalchemy_pagination import paginate

        page = paginate(session.query(User), 1, 25)
    """
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    # We remove the ordering of the query since it doesn't matter for getting
    # a count and might have performance implications as discussed on
    # this Flask-SqlAlchemy issue
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/100
    total = query.order_by(None).count()
    return Page(items, page, page_size, total)
