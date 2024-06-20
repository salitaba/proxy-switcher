import json
from datetime import timedelta

import requests
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView


class ProxySwitcher:
    proxy_index = 0
    proxy_list = []
    latest_update = timezone.now()

    @classmethod
    def get_proxy(cls):
        if timezone.now() - cls.latest_update >= timedelta(days=1) or len(cls.proxy_list) == 0:
            cls.update_proxy()
        return cls.proxy_list[cls.proxy_index]

    @classmethod
    def update_proxy(cls):
        cls.proxy_list = open("out/proxies/all.txt").read().splitlines()
        cls.proxy_index = 0
        cls.latest_update = timezone.now()

    @classmethod
    def call_request(cls, url, headers=None, method='GET', body=None, max_retries=2):
        num_retries = 0
        while num_retries < max_retries:
            commons = {
                "headers": headers,
                "proxies": dict(http=cls.get_proxy(), https=cls.get_proxy()),
                "timeout": 10
            }
            try:
                if method == 'GET':
                    return requests.get(url, **commons)
                else:
                    return requests.post(url, data=json.dumps(body), **commons)
            except Exception as e:
                print(e)
                cls.proxy_index = (cls.proxy_index + 1) % len(cls.proxy_list)
                num_retries += 1
        return requests.get(url)


class ProxyView(APIView):

    def post(self, request, *args, **kwargs):
        url = request.data.get("url", None)
        headers = request.data.get("headers", None)
        method = request.data.get("method", "GET")
        if url:
            response = ProxySwitcher.call_request(url, headers, method)
            headers = {"Location": response.headers.get("Location")} if response.headers.get("Location") else {}
            if response.headers.get("Content-Type"):
                headers["Content-Type"] = response.headers.get("Content-Type")
            return HttpResponse(response.content, status=response.status_code, headers=headers)
        else:
            return Response({"error": "URL must be provided"}, status=200)
