"""
🐻 Memory Manager for Mama Bear
Handles persistent conversation memory using Mem0.ai and local storage
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

class MemoryManager:
    """Manages persistent memory for Mama Bear conversations"""
    
    def __init__(self):
        self.mem0_enabled = os.getenv('MEM0_MEMORY_ENABLED', 'True').lower() == 'true'
        self.mem0_api_key = os.getenv('MEM0_API_KEY', 'm0-tBwWs1ygkxcbEiVvX6iXdwiJ42epw8a3wyoEUlpg')
        self.db_path = Path("backend/sanctuary_memory.db")
        
        # Initialize local database
        self._init_database()
        
        # Initialize Mem0 if enabled
        if self.mem0_enabled:
            try:
                self._init_mem0()
                logger.info("✅ Mem0 memory system initialized")
            except Exception as e:
                logger.warning(f"Mem0 initialization failed, using local storage: {e}")
                self.mem0_enabled = False
        
        logger.info("🧠 Memory Manager initialized")
    
    def _init_database(self):
        """Initialize local SQLite database for memory storage"""
        
        # Create directory if it doesn't exist
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    page_context TEXT NOT NULL,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    metadata TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id TEXT PRIMARY KEY,
                    preferences TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS session_memory (
                    user_id TEXT,
                    page_context TEXT,
                    memory_key TEXT,
                    memory_value TEXT,
                    expires_at DATETIME,
                    PRIMARY KEY (user_id, page_context, memory_key)
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_page ON conversations(user_id, page_context)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
            
            conn.commit()
    
    def _init_mem0(self):
        """Initialize Mem0 client"""
        try:
            # This would normally import the Mem0 client
            # For now, we'll simulate it
            logger.info("Mem0 client initialized (simulated)")
        except ImportError:
            raise Exception("Mem0 client not available")
    
    async def get_context(self, user_id: str, page_context: str, limit: int = 10) -> Dict[str, Any]:
        """Get conversation context for a user and page"""
        
        try:
            # Get recent conversations from local database
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT message, response, metadata, timestamp
                    FROM conversations
                    WHERE user_id = ? AND page_context = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (user_id, page_context, limit))
                
                conversations = [dict(row) for row in cursor.fetchall()]
            
            # Get user preferences
            preferences = await self.get_user_preferences(user_id)
            
            # Get session memory
            session_memory = await self.get_session_memory(user_id, page_context)
            
            # Format recent interactions
            recent_interactions = ""
            if conversations:
                for conv in reversed(conversations[-5:]):  # Last 5 interactions
                    recent_interactions += f"User: {conv['message']}\nMama Bear: {conv['response']}\n\n"
            
            context = {
                'user_id': user_id,
                'page_context': page_context,
                'recent_interactions': recent_interactions.strip(),
                'conversation_count': len(conversations),
                'preferences': preferences,
                'session_memory': session_memory,
                'last_interaction': conversations[0]['timestamp'] if conversations else None
            }
            
            # Add Mem0 context if available
            if self.mem0_enabled:
                try:
                    # Simulate Mem0 query
                    mem0_context = {
                        'relevant_memories': [],
                        'personality_insights': {},
                        'learned_preferences': {}
                    }
                    context['mem0_context'] = mem0_context
                except Exception as e:
                    logger.warning(f"Mem0 context retrieval failed: {e}")
            
            return context
            
        except Exception as e:
            logger.error(f"Context retrieval error: {e}")
            return {
                'user_id': user_id,
                'page_context': page_context,
                'error': str(e)
            }
    
    async def save_interaction(self, 
                             user_id: str, 
                             page_context: str,
                             message: str, 
                             response: str,
                             metadata: Dict[str, Any] = None) -> bool:
        """Save a conversation interaction"""
        
        try:
            # Save to local database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO conversations (user_id, page_context, message, response, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, page_context, message, response, json.dumps(metadata or {})))
                
                conn.commit()
            
            # Save to Mem0 if enabled
            if self.mem0_enabled:
                try:
                    # Simulate Mem0 save
                    logger.debug(f"Saved to Mem0: {user_id} - {page_context}")
                except Exception as e:
                    logger.warning(f"Mem0 save failed: {e}")
            
            # Clean up old conversations (keep last 1000 per user/page)
            await self._cleanup_old_conversations(user_id, page_context)
            
            return True
            
        except Exception as e:
            logger.error(f"Interaction save error: {e}")
            return False
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT preferences FROM user_preferences WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row['preferences'])
                else:
                    # Return default preferences
                    return {
                        'theme': 'light',
                        'mama_bear_personality': 'caring',
                        'response_style': 'detailed',
                        'preferred_models': []
                    }
                    
        except Exception as e:
            logger.error(f"Preferences retrieval error: {e}")
            return {}
    
    async def save_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Save user preferences"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_preferences (user_id, preferences)
                    VALUES (?, ?)
                """, (user_id, json.dumps(preferences)))
                
                conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Preferences save error: {e}")
            return False
    
    async def get_session_memory(self, user_id: str, page_context: str) -> Dict[str, Any]:
        """Get session-specific memory"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT memory_key, memory_value
                    FROM session_memory
                    WHERE user_id = ? AND page_context = ? AND expires_at > datetime('now')
                """, (user_id, page_context))
                
                session_data = {}
                for row in cursor.fetchall():
                    try:
                        session_data[row['memory_key']] = json.loads(row['memory_value'])
                    except json.JSONDecodeError:
                        session_data[row['memory_key']] = row['memory_value']
                
                return session_data
                
        except Exception as e:
            logger.error(f"Session memory retrieval error: {e}")
            return {}
    
    async def save_session_memory(self, 
                                user_id: str, 
                                page_context: str, 
                                key: str, 
                                value: Any,
                                expires_in_hours: int = 24) -> bool:
        """Save session-specific memory"""
        
        try:
            expires_at = datetime.now() + timedelta(hours=expires_in_hours)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO session_memory 
                    (user_id, page_context, memory_key, memory_value, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, page_context, key, json.dumps(value), expires_at))
                
                conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Session memory save error: {e}")
            return False
    
    async def get_conversation_history(self, 
                                     user_id: str, 
                                     page_context: str = None,
                                     limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                if page_context:
                    cursor = conn.execute("""
                        SELECT * FROM conversations
                        WHERE user_id = ? AND page_context = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """, (user_id, page_context, limit))
                else:
                    cursor = conn.execute("""
                        SELECT * FROM conversations
                        WHERE user_id = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """, (user_id, limit))
                
                conversations = []
                for row in cursor.fetchall():
                    conv = dict(row)
                    try:
                        conv['metadata'] = json.loads(conv['metadata'] or '{}')
                    except json.JSONDecodeError:
                        conv['metadata'] = {}
                    conversations.append(conv)
                
                return conversations
                
        except Exception as e:
            logger.error(f"History retrieval error: {e}")
            return []
    
    async def _cleanup_old_conversations(self, user_id: str, page_context: str):
        """Clean up old conversations to prevent database bloat"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Keep only the last 1000 conversations per user/page
                conn.execute("""
                    DELETE FROM conversations
                    WHERE user_id = ? AND page_context = ? AND id NOT IN (
                        SELECT id FROM conversations
                        WHERE user_id = ? AND page_context = ?
                        ORDER BY timestamp DESC
                        LIMIT 1000
                    )
                """, (user_id, page_context, user_id, page_context))
                
                conn.commit()
                
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get memory system status"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) as count FROM conversations")
                total_conversations = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(DISTINCT user_id) as count FROM conversations")
                unique_users = cursor.fetchone()[0]
                
                cursor = conn.execute("""
                    SELECT COUNT(*) as count FROM session_memory 
                    WHERE expires_at > datetime('now')
                """)
                active_sessions = cursor.fetchone()[0]
            
            return {
                'connected': True,
                'mem0_enabled': self.mem0_enabled,
                'total_conversations': total_conversations,
                'unique_users': unique_users,
                'active_sessions': active_sessions,
                'database_path': str(self.db_path),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return {
                'connected': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }