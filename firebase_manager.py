"""
Firebase/Firestore manager for state persistence and real-time updates.
Implements robust error handling and connection management.
"""
import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from google.cloud import firestore
from google.cloud.firestore_v1 import Client
from google.api_core.exceptions import GoogleAPICallError, RetryError
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

from config import config

logger = logging.getLogger(__name__)

class FirebaseManager:
    """Manages Firebase connections and operations with fault tolerance"""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._initialize_firebase()
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection with error handling"""
        try:
            creds_path = config.get("database").firebase_credentials_path
            
            if not config.validate_firebase_credentials():
                raise FileNotFoundError(f"Firebase credentials not found at {creds_path}")
            
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate(creds_path)
                firebase_admin.initialize_app(cred)
            
            self._client = firestore.client()
            logger.info("Firebase Firestore initialized successfully")
            
        except (FileNotFoundError, FirebaseError, GoogleAPICallError) as e:
            logger.error(f"Failed to initialize Firebase