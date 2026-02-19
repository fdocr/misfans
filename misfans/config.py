import os
from dataclasses import dataclass

@dataclass
class Config:
    FAN_PIN: int = int(os.getenv('FAN_PIN', '4'))
    POLL_INTERVAL: float = float(os.getenv('POLL_INTERVAL', '5'))
    ON_TEMP: float = float(os.getenv('ON_TEMP', '55'))
    OFF_TEMP: float = float(os.getenv('OFF_TEMP', '50'))
    RUN_USER: str = os.getenv('RUN_USER', 'misfans')

config = Config()
