from rest_framework.pagination import CursorPagination


class Pagination(CursorPagination):
  cursor_query_param = 'cursor'
  page_size = 30
  ordering = '-id'

  page_size_query_param = None

  max_page_size = 50
