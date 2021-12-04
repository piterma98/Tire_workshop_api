"""Pagination."""
# 3rd-party
from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    """Custom pagination."""

    page_size = 10
