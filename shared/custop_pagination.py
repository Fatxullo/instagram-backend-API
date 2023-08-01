from rest_framework.pagination import PageNumberPagination # in bari bisyor postoya yagranda nochigid kam kam chigidan bari shah programa sekin nashudanish
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):   # in class bari postoya kam kam return karan
    page_size = 10               # in bari yagranda 10- ta posta return karan - hudomo chanta hohem navisem meshad injaba bari yagranda chana return karanish
    page_size_query_param = 'page_size' 
    max_page_size = 100     # you want or dont want but this is max posts that can return greather than 100-False
    
    def get_paginated_response(self, data):
        return Response(
            {
                'next': self.get_next_link(),
                'pervious': self.get_previous_link(),
                'count': self.page.paginator.count,
                'results': data
            }
        )