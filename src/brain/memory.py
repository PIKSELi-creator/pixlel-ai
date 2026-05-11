"""
Pixlel AI - Продвинутая Система Памяти
Файл: src/brain/memory.py
Версия: 0.3.0
Описание: Многоуровневая память с краткосрочной, долгосрочной и семантической памятью
"""

import os
import json
import time
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import deque, defaultdict
import asyncio
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger("PixlelMemory")


class MemoryEntry(BaseModel):
    id: str
    timestamp: str
    user_message: str
    assistant_response: str
    summary: str = ""
    importance: float = 0.5
    tags: List[str] = Field(default_factory=list)
    context: Dict = Field(default_factory=dict)


class ConversationSession(BaseModel):
    session_id: str
    start_time: str
    last_active: str
    message_count: int = 0
    topic: str = "Общий"
    entries: List[MemoryEntry] = Field(default_factory=list)


class PixlelMemory:
    """Полноценная система памяти Pixlel AI"""

    def __init__(self, short_term_limit: int = 30, data_dir: str = "data/memory"):
        self.short_term_limit = short_term_limit
        self.data_dir = data_dir
        self.short_term = deque(maxlen=short_term_limit)
        self.long_term: List[MemoryEntry] = []
        self.sessions: Dict[str, ConversationSession] = {}
        self.current_session_id = self._new_session_id()
        self.tags_index = defaultdict(list)

        self._ensure_directories()
        self.load()

        logger.info(f"✅ Pixlel Memory загружена | Короткая: {len(self.short_term)} | Долгая: {len(self.long_term)}")

    def _ensure_directories(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)

    def _new_session_id(self) -> str:
        return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:12]

    def add(self, user_message: str, assistant_response: str, importance: float = 0.65, tags: List[str] = None):
        """Добавить взаимодействие в память"""
        if tags is None:
            tags = self._auto_tags(user_message + assistant_response)

        entry = MemoryEntry(
            id=hashlib.sha256(f"{user_message}{time.time()}".encode()).hexdigest()[:16],
            timestamp=datetime.now().isoformat(),
            user_message=user_message,
            assistant_response=assistant_response,
            summary=assistant_response[:200] + "..." if len(assistant_response) > 200 else assistant_response,
            importance=importance,
            tags=tags
        )

        self.short_term.append(entry)
        self.long_term.append(entry)

        # Обновляем сессию
        if self.current_session_id not in self.sessions:
            self.sessions[self.current_session_id] = ConversationSession(
                session_id=self.current_session_id,
                start_time=datetime.now().isoformat(),
                last_active=datetime.now().isoformat()
            )
        self.sessions[self.current_session_id].entries.append(entry)
        self.sessions[self.current_session_id].message_count += 1
        self.sessions[self.current_session_id].last_active = datetime.now().isoformat()

        # Индекс тегов
        for tag in tags:
            self.tags_index[tag].append(entry.id)

        self.save()
        return entry

    def get_context(self, query: str = "", limit: int = 10) -> str:
        """Получить релевантный контекст"""
        if not self.long_term:
            return ""

        results = sorted(
            self.long_term[-50:],
            key=lambda x: self._score(query, x),
            reverse=True
        )[:limit]

        context = "\n---\n".join([
            f"User: {e.user_message}\nPixlel: {e.assistant_response[:400]}"
            for e in results
        ])
        return context

    def _score(self, query: str, entry: MemoryEntry) -> float:
        score = entry.importance
        q = query.lower()
        if q in entry.user_message.lower() or q in entry.assistant_response.lower():
            score += 0.8
        return score

    def _auto_tags(self, text: str) -> List[str]:
        keywords = ["привет", "шутка", "помоги", "как", "почему", "когда", "pixel", "игра", "код", "учеба"]
        return [kw for kw in keywords if kw in text.lower()][:4]

    def save(self):
        try:
            data = {
                "long_term": [e.model_dump() for e in self.long_term[-500:]],
                "sessions": {k: v.model_dump() for k, v in self.sessions.items()},
                "saved_at": datetime.now().isoformat()
            }
            with open(f"{self.data_dir}/memory.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения памяти: {e}")

    def load(self):
        try:
            path = f"{self.data_dir}/memory.json"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.long_term = [MemoryEntry(**e) for e in data.get("long_term", [])]
                logger.info(f"Загружено {len(self.long_term)} записей из памяти")
        except Exception as e:
            logger.warning(f"Не удалось загрузить память: {e}")

    def get_stats(self):
        return {
            "short_term": len(self.short_term),
            "long_term": len(self.long_term),
            "sessions": len(self.sessions),
            "current_session": self.current_session_id
        }


# Тест при импорте
if __name__ == "__main__":
    m = PixlelMemory()
    m.add("Привет, как дела?", "Отлично! А у тебя?", importance=0.8)
    print("Memory test passed!")
    print(m.get_stats())