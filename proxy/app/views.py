from datetime import timedelta

import requests
from django.http import HttpResponse
from django.utils import timezone
from django.views import View


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
    def call_request(cls, target_url, max_retries=2):
        num_retries = 0
        while num_retries < max_retries:
            try:
                return requests.get(target_url, proxies=dict(http=cls.get_proxy(), https=cls.get_proxy()), timeout=10)
            except Exception as e:
                print(e)
                cls.proxy_index = (cls.proxy_index + 1) % len(cls.proxy_list)
                num_retries += 1
        return requests.get(target_url)


class ProxyView(View):

    def get(self, request, *args, **kwargs):
        target_url = request.COOKIES.get('target_url', None)
        if target_url:
            response = ProxySwitcher.call_request(target_url)
            headers = {"Location": response.headers.get("Location")} if response.headers.get("Location") else {}
            if response.headers.get("Content-Type"):
                headers["Content-Type"] = response.headers.get("Content-Type")
            return HttpResponse(response.content, status=response.status_code, headers=headers)
        else:
            return HttpResponse("Set target_url in cookie")
