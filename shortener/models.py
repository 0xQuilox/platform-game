from dataclasses import dataclass, field
from typing import Any

class Short_URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    return url_map.get(short_code)