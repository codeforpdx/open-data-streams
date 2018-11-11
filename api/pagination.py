from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class LimitOffsetPaginationDataOnly(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response(data)

