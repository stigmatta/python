import math

from controllers.controller_rest import ControllerRest
from controllers.rest_error import RestError
from controllers.rest_response import RestLink, RestMeta, RestPagination

products = [
    {"id": 1, "name": "Product 1", "price": 99.9 },
    {"id": 2, "name": "Product 2", "price": 199.9 },
    {"id": 3, "name": "Product 3", "price": 299.9 },
    {"id": 4, "name": "Product 4", "price": 399.9 },
    {"id": 5, "name": "Product 5", "price": 499.9 },
    {"id": 6, "name": "Product 6", "price": 599.9 },
    {"id": 7, "name": "Product 7", "price": 699.9 },
    {"id": 8, "name": "Product 8", "price": 799.9 },
    {"id": 9, "name": "Product 9", "price": 899.9 },
    {"id": 10, "name": "Product 10", "price": 999.9 },
    {"id": 11, "name": "Product 11", "price": 1099.9 },
    {"id": 12, "name": "Product 12", "price": 1199.9 }
]

class ProductController(ControllerRest):
    # pagination
    # - total items
    # - items per page
    # - total pages
    # - page number

    def do_GET(self):
        per_page = self.query_params.get('perpage', 5)  # default 5 
        if not isinstance(per_page, int):
            try:
                per_page = int(per_page)
            except ValueError:
                per_page = 0

        if per_page <= 0:
            raise RestError(400, "Bad request", "Invalid 'perpage' parameter")
        
    
        total_items = len(products)
        total_pages = math.ceil(total_items / per_page)

        page = self.query_params.get('page', 1)  # default 1
        if not isinstance(page, int):
            try:
                page = int(page)
            except ValueError:
                page = 0
        
        if page <= 0 or page > total_pages:
            raise RestError(400, "Bad request", f"Invalid 'page' parameter (must be in range 1 - {total_pages})")

        has_prev_page = True if page > 1 else False
        has_next_page = True if page < total_pages else False

        
        self.rest_response.meta = RestMeta(
            pagination=RestPagination(
                per_page,
                page,
                total_items,
                total_pages,
                has_prev_page,
                has_next_page
            ),
            links=[
                RestLink("1", f"?perpage={per_page}"),
                RestLink(str(total_pages), f"?page={total_pages}&perpage={per_page}"),
                RestLink(str(page + 1), f"?page={page+1}&perpage={per_page}") if page < total_pages else None,
                RestLink(str(page - 1), f"?page={page-1}&perpage={per_page}") if page > 1 else None
            ]
        )

        self.rest_response.data = products[(page-1)*per_page : page*per_page]

        

