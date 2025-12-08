# config/cors_middleware.py
from django.http import HttpResponse


def SimpleCORSMiddleware(get_response):
    """
    非常用の簡易 CORS ミドルウェア。
    全レスポンスに CORS ヘッダを付ける。
    プロダクション用というより、まずは PoC 用。
    """

    def middleware(request):
        # OPTIONS の場合はプリフライト用に空レスポンスでもOK
        if request.method == "OPTIONS":
            response = HttpResponse()
        else:
            response = get_response(request)

        origin = request.headers.get("Origin")
        if origin:
            # 今回は来た Origin をそのまま返す（フロントが1つなのでOK）
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"

        # 許可メソッド
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

        # 許可ヘッダ（プリフライトで要求されているヘッダをそのまま返す）
        request_headers = request.headers.get("Access-Control-Request-Headers")
        if request_headers:
            response["Access-Control-Allow-Headers"] = request_headers
        else:
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        # 認証情報を含める場合
        response["Access-Control-Allow-Credentials"] = "true"

        return response

    return middleware
