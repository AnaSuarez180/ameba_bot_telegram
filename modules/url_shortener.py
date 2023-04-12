import pyshorteners
from pyshorteners import exceptions


class UrlShortener:
    def __init__(self):
        self.services = {
            'tinyurl': {'function': 'short', 'module': 'tinyurl', 'name': 'TinyURL'},
            'clckru': {'function': 'short', 'module': 'clckru', 'name': 'Clck.ru'},
            'chilpit': {'function': 'short', 'module': 'chilpit', 'name': 'Chilp.it'},
            'cuttly': {'function': 'short', 'module': 'cuttly', 'name': 'Cutt.ly'}
        }

    def shorten_url(self, url, service):
        if service not in self.services:
            raise ValueError(f"Service '{service}' not supported")

        s = pyshorteners.Shortener()
        service_info = self.services[service]
        try:
            short_url = getattr(getattr(s, service_info['module']), service_info['function'])(url=url)
        except exceptions.ShorteningErrorException as e:
            raise ValueError(f"Error shortening URL with {service_info['name']}: {e}")

        return short_url