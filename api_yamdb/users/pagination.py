from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20

    # FOR CUSTOM PAGINATION
    # def get_paginated_response(self, data):
    #     return JsonResponse({
    #         'count': self.page.paginator.count,
    #         'next': self.get_next_link(),
    #         'previous': self.get_previous_link(),
    #         'results': data
    #     })

