import json
import os
from .errors import DuplicateTableError, TableNotFoundError

class Table:
    def __init__(self, name: str):
        self.name = name
        self.filename = f"{name}.json"
        self.data: dict[str, list[str]] = {}
        self.sort_order: str | None = None
        self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def write(self, key: str, content: str):
        parts = content.split()
        if key in self.data:
            self.data[key].extend(parts)
        else:
            self.data[key] = parts
        self._save()

    def read(self, filters: list[str] | None = None):
        if filters is None:
            keys = list(self.data.keys())
        else:
            keys = [k for k in filters if k in self.data]

        if self.sort_order == 'asc':
            keys.sort()
        elif self.sort_order == 'desc':
            keys.sort(reverse=True)

        return {k: self.data[k] for k in keys}

    def delete(self, keys: list[str]):
        for k in keys:
            if k in self.data:
                del self.data[k]
        self._save()

    def set_sort(self, order: str | None):
        if order in ('asc', 'desc', None):
            self.sort_order = order
            self._save()
