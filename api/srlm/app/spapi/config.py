"""Provides easy access to the API by creating methods that inject the authorization headers"""
import os
import requests


class SlapAPI:
    api_url = os.getenv('SLAP_API_URL')
    api_key = os.getenv('SLAP_API_KEY')
    headers = {"Authorization": f"Bearer {api_key}"}

    def post(self, endpoint, json):
        return requests.post(f'{self.api_url}{endpoint}', json=json, headers=self.headers)

    def get(self, endpoint):
        return requests.get(f'{self.api_url}{endpoint}', headers=self.headers)

    def delete(self, endpoint):
        return requests.delete(f'{self.api_url}{endpoint}', headers=self.headers)
