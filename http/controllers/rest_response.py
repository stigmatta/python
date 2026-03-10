import math


class RestStatus:
    def __init__(self, is_ok:bool=True, code:int=200, phrase:str="OK"):
        self.is_ok = is_ok
        self.code = code
        self.phrase = phrase

    def __json__(self):
        return {
            "is_ok": self.is_ok,
            "code": self.code,
            "phrase": self.phrase
        }
    
RestStatus.ok_200 = RestStatus(True, 200, "OK")
RestStatus.created_201 = RestStatus(True, 201, "Created")
RestStatus.no_content_204 = RestStatus(True, 204, "No Content")

RestStatus.bad_request_400 = RestStatus(False, 400, "Bad Request")
RestStatus.unauthorized_401 = RestStatus(False, 401, "Unauthorized")
RestStatus.forbidden_403 = RestStatus(False, 403, "Forbidden")
RestStatus.not_found_404 = RestStatus(False, 404, "Not Found")
RestStatus.method_not_allowed_405 = RestStatus(False, 405, "Method Not Allowed")
RestStatus.unsupported_media_415 = RestStatus(False, 415, "Unsupported Media Type")

RestStatus.internal_error_500 = RestStatus(False, 500, "Internal Server Error")
RestStatus.service_unavailable_503 = RestStatus(False, 503, "Service Unavailable")


class RestLink:
    def __init__(self, name:str, url:str):
        self.name = name
        self.url = url
    

    def __json__(self):
        return {
            "name": self.name,
            "url": self.url
        }

class RestPagination:
    def __init__(self, per_page:int, page:int, total_items:int, total_pages:int|None,
                 has_prev_page:bool, has_next_page:bool,links:list[RestLink]|None=None):
        self.per_page = per_page
        self.page = page
        self.total_items = total_items
        self.total_pages = total_pages if total_pages is not None else math.ceil(total_items / per_page)
        self.has_prev_page = has_prev_page
        self.has_next_page = has_next_page
        self.links = links


    def __json__(self):
        return {
            "perPage": self.per_page,
            "currentPage": self.page,
            "totalItems": self.total_items,
            "totalPages": self.total_pages,
            "hasPrevPage": self.has_prev_page,
            "hasNextPage": self.has_next_page,
            "links": self.links
        }

class RestMeta:
    def __init__(self, pagination:RestPagination|None=None, links:list[RestLink]|None=None):
        self.pagination = pagination
        self.links = links

    def __json__(self):
        return {
            "pagination": self.pagination,
            "links": self.links
        }

class RestResponse:
    def __init__(self, status:RestStatus|None=None, meta:RestMeta|None=None, data:any=None):
        self.status = status if status is not None else RestStatus()
        self.meta = meta if meta is not None else RestMeta()
        self.data = data

    def __json__(self):
        return {
            "status": self.status,
            "meta": self.meta,
            "data": self.data
        }