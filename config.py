"""
Configuration management for the Autonomous Evolutionary Strategy Engine.
Centralizes environment variables and configuration settings with validation.
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class DatabaseConfig:
    """Firebase/Firestore configuration"""
    firebase_credentials_path: str
    firestore_collection_prefix: str = "evolution_strategies"
    
@dataclass
class MarketConfig:
    """Market data and exchange configuration"""
    exchange_id: str = "binance"
    symbols: list = None
    timeframe: str = "1h"
    historical_days: int = 30
    
    def __post_init__(self):
        if self.symbols is None:
            self.symbols = ["BTC/USDT", "ETH/USDT"]

@dataclass
class RLConfig:
    """Reinforcement learning configuration"""
    learning_rate: float = 0.001
    discount_factor: float = 0.99
    exploration_rate: float = 0.1
    memory_size: int = 10000
    batch_size: int = 32
    
@dataclass
class LoggingConfig:
    """Logging configuration"""
    log_level: str = "INFO"
    log_file: str = "evolution_engine.log"
    max_file_size_mb: int = 10
    backup_count: int = 5

class ConfigManager:
    """Manages configuration loading and validation"""
    
    def __init__(self):
        self._config = {}
        self._validate_environment()
        self._load_config()
        
    def _validate_environment(self) -> None:
        """Validate required environment variables"""
        required_vars = [
            "FIREBASE_CREDENTIALS_PATH",
            "EXCHANGE_API_KEY",
            "EXCHANGE_SECRET"
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
            
    def _load_config(self) -> None:
        """Load and validate all configurations"""
        try:
            self._config = {
                "database": DatabaseConfig(
                    firebase_credentials_path=os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json"),
                    firestore_collection_prefix=os.getenv("FIRESTORE_PREFIX", "evolution_strategies")
                ),
                "market": MarketConfig(
                    exchange_id=os.getenv("EXCHANGE_ID", "binance"),
                    symbols=os.getenv("SYMBOLS", "BTC/USDT,ETH/USDT").split(","),
                    timeframe=os.getenv("TIMEFRAME", "1h"),
                    historical_days=int(os.getenv("HISTORICAL_DAYS", "30"))
                ),
                "rl": RLConfig(
                    learning_rate=float(os.getenv("LEARNING_RATE", "0.001")),
                    discount_factor=float(os.getenv("DISCOUNT_FACTOR", "0.99")),
                    exploration_rate=float(os.getenv("EXPLORATION_RATE", "0.1")),
                    memory_size=int(os.getenv("MEMORY_SIZE", "10000")),
                    batch_size=int(os.getenv("BATCH_SIZE", "32"))
                ),
                "logging": LoggingConfig(
                    log_level=os.getenv("LOG_LEVEL", "INFO"),
                    log_file=os.getenv("LOG_FILE", "evolution_engine.log"),
                    max_file_size_mb=int(os.getenv("MAX_LOG_SIZE_MB", "10")),
                    backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5"))
                ),
                "api_keys": {
                    "exchange_api_key": os.getenv("EXCHANGE_API_KEY"),
                    "exchange_secret": os.getenv("EXCHANGE_SECRET")
                }
            }
        except (ValueError, TypeError) as e:
            raise ValueError(f"Configuration error: {e}")
            
    def get(self, section: str) -> Any:
        """Get configuration section"""
        if section not in self._config:
            raise KeyError(f"Configuration section '{section}' not found")
        return self._config[section]
        
    def validate_firebase_credentials(self) -> bool:
        """Validate Firebase credentials file exists"""
        creds_path = self._config["database"].firebase_credentials_path
        return os.path.exists(creds_path)

# Singleton instance
config = ConfigManager()