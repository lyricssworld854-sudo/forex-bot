import json
import os
from typing import Dict, List


class AlertManager:
    def __init__(self, storage_file: str = "alerts.json"):
        self.storage_file = storage_file
        self.alerts: Dict[int, List[dict]] = self._load_alerts()

    def _load_alerts(self) -> dict:
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    return {int(k): v for k, v in data.items()}
            except Exception:
                return {}
        return {}

    def _save_alerts(self):
        with open(self.storage_file, 'w') as f:
            json.dump({str(k): v for k, v in self.alerts.items()}, f)

    def add_alert(self, user_id: int, pair: str, target_price: float):
        if user_id not in self.alerts:
            self.alerts[user_id] = []
        self.alerts[user_id].append({
            'pair': pair,
            'target': target_price,
            'active': True
        })
        self._save_alerts()

    def remove_alert(self, user_id: int, pair: str, target_price: float):
        if user_id in self.alerts:
            self.alerts[user_id] = [
                a for a in self.alerts[user_id]
                if not (a['pair'] == pair and a['target'] == target_price)
            ]
            self._save_alerts()

    def get_user_alerts(self, user_id: int) -> list:
        return self.alerts.get(user_id, [])

    def get_all_alerts(self) -> dict:
        return self.alerts
