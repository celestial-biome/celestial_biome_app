# config/middleware.py
from django.http import HttpResponse

def SimpleCorsDebugMiddleware(get_response):
    def middleware(request):
        # OPTIONS の場合は空レスポンスでもOK
        if request.method == "OPTIONS":
            response = HttpResponse()
        else:
            response = get_response(request)

        origin = request.headers.get("Origin")
        if origin:
            # 今回はフロントからの Origin をそのまま返す
            response["Access-Control-Allow-Origin"] = origin

        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"

        return response

    return middleware
