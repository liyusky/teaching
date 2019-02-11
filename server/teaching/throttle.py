from rest_framework.throttling import SimpleRateThrottle


class SMSSendThrottle(SimpleRateThrottle):
    rate = '1/m'

    def get_cache_key(self, request, view):
        return request.data['phone']