from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

BASE_URL = "https://mainofficial-i-game.com.cn"
CORE_TAG = "爱游戏"


@dataclass
class KeywordNote:
    keyword: str
    description: str
    source_url: str = BASE_URL
    tags: List[str] = field(default_factory=lambda: [CORE_TAG])
    created_at: Optional[str] = None
    importance: int = 5

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.importance < 1:
            self.importance = 1
        elif self.importance > 10:
            self.importance = 10

    def summary(self) -> str:
        return f"[{self.keyword}] ({self.importance}/10) - {self.description[:50]}..."

    def full_info(self) -> str:
        tag_line = ", ".join(self.tags)
        return (
            f"关键词：{self.keyword}\n"
            f"描述：{self.description}\n"
            f"来源：{self.source_url}\n"
            f"标签：{tag_line}\n"
            f"创建时间：{self.created_at}\n"
            f"重要性：{self.importance}/10"
        )


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_importance(self, min_imp: int = 1, max_imp: int = 10) -> List[KeywordNote]:
        return [n for n in self.notes if min_imp <= n.importance <= max_imp]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all(self, compact: bool = False) -> str:
        if not self.notes:
            return "（暂无笔记）"
        lines = []
        for i, note in enumerate(self.notes, 1):
            if compact:
                lines.append(f"{i}. {note.summary()}")
            else:
                lines.append(f"--- 笔记 {i} ---")
                lines.append(note.full_info())
                lines.append("")
        return "\n".join(lines)


def create_sample_notes() -> NoteCollection:
    return NoteCollection(notes=[
        KeywordNote(
            keyword="爱游戏平台",
            description="爱游戏是一个综合性游戏服务平台，提供丰富多样的游戏内容和社区互动功能。",
            source_url=BASE_URL,
            tags=[CORE_TAG, "游戏平台"],
            importance=9,
        ),
        KeywordNote(
            keyword="游戏资讯",
            description="每日更新最新的游戏新闻、攻略评测和活动预告，帮助玩家掌握第一手信息。",
            source_url=f"{BASE_URL}/news",
            tags=[CORE_TAG, "资讯"],
            importance=7,
        ),
        KeywordNote(
            keyword="社区互动",
            description="玩家可以在这里发帖、留言、组队，共同分享游戏心得与乐趣。",
            source_url=f"{BASE_URL}/community",
            tags=[CORE_TAG, "社区"],
            importance=6,
        ),
        KeywordNote(
            keyword="新手引导",
            description="为初次使用爱游戏平台的用户提供详细的操作指引和常见问题解答。",
            source_url=f"{BASE_URL}/guide",
            tags=[CORE_TAG, "帮助"],
            importance=8,
        ),
        KeywordNote(
            keyword="版本更新",
            description="记录爱游戏平台各版本的功能更新、优化内容和问题修复日志。",
            source_url=f"{BASE_URL}/changelog",
            tags=[CORE_TAG, "更新"],
            importance=5,
        ),
    ])


if __name__ == "__main__":
    collection = create_sample_notes()
    print("【完整格式】")
    print(collection.format_all(compact=False))
    print("\n【简洁格式】")
    print(collection.format_all(compact=True))
    print("\n【按重要性筛选（>=7）】")
    for n in collection.filter_by_importance(min_imp=7):
        print(n.summary())