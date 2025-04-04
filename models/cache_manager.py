import json
from datetime import datetime, timedelta
import os

class CacheManager:
    def __init__(self, cache_file='citas_cache.json', cache_duration=15):
        self.cache_file = cache_file
        self.cache_duration = timedelta(minutes=cache_duration)
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                try:
                    data = json.load(f)
                    data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                    return data
                except (json.JSONDecodeError, KeyError):
                    pass
        return {'data': None, 'timestamp': None}

    def _save_cache(self):
        cache_data = {
            'data': self.cache['data'],
            'timestamp': self.cache['timestamp'].isoformat()
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)

    def get_data(self):
        if self.cache['data'] and self._is_cache_valid():
            return self.cache['data']
        return None

    def update_cache(self, new_data):
        self.cache = {
            'data': new_data,
            'timestamp': datetime.now()
        }
        self._save_cache()

    def _is_cache_valid(self):
        return (datetime.now() - self.cache['timestamp']) < self.cache_duration