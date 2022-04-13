from typing import Callable, Optional, List, Any, TypeVar
import time

T = TypeVar("T")

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x

class Event:
    """Meta: Raw payload of the generated event"""
    raw: str
    """UGC: Event content text"""
    content: Optional[str]
    """Meta: UNIX Timestamp of when the event was created (i.e when a message was sent)"""
    created_at: Optional[float]
    """Meta: Hostname of source"""
    hostname: Optional[str]
    """Meta: IP address of source"""
    ip: Optional[str]
    """UGC: Unique identifier provided by source platform (e.g Post ID, Message ID)"""
    originating_id: Optional[str]
    """Meta: UNIX Timestamp of when we found the event"""
    parse_time: Optional[float]
    """Meta: Endpoint from which the event came from"""
    path: str
    """Meta: Producer module name"""
    producer: str
    """UGC: IDs of associated users in event (Comment reply, message reply)"""
    relationships: Optional[List[str]]
    """UGC: User's follower count"""
    statistics_followers: Optional[float]
    """UGC: Content other interactions (e.g reply count)"""
    statistics_interactions: Optional[float]
    """UGC: Content negative interactions"""
    statistics_negative: Optional[float]
    """UGC: Content positive interactions"""
    statistics_positive: Optional[float]
    statistics_republish: Optional[float]
    """UGC: Content view count"""
    statistics_views: Optional[float]
    """UGC: Tags provided by user"""
    tags: Optional[List[str]]
    """Meta: Type of event (Message/Comment/Found Site)"""
    type: str
    """UGC: ID of the creator of the event (including when the event is a user)"""
    user_id: Optional[str]
    """UGC: Creator username"""
    username: Optional[str]

    def __init__(self, raw: str, content: Optional[str], created_at: Optional[float], hostname: Optional[str], ip: Optional[str], originating_id: Optional[str], parse_time: Optional[float], path: str, producer: str, relationships: Optional[List[str]], statistics_followers: Optional[float], statistics_interactions: Optional[float], statistics_negative: Optional[float], statistics_positive: Optional[float], statistics_republish: Optional[float], statistics_views: Optional[float], tags: Optional[List[str]], type: str, user_id: Optional[str], username: Optional[str]) -> None:
        self.raw = raw
        self.content = content
        self.hostname = hostname
        self.ip = ip
        self.originating_id = originating_id
        if (parse_time):
            self.parse_time = parse_time
        else:
            self.parse_time = int(time.now())
        self.path = path
        self.producer = producer
        self.relationships = relationships
        self.statistics_followers = statistics_followers
        self.statistics_interactions = statistics_interactions
        self.statistics_negative = statistics_negative
        self.statistics_positive = statistics_positive
        self.statistics_republish = statistics_republish
        self.statistics_views = statistics_views
        self.tags = tags
        self.created_at = created_at
        self.type = type
        self.user_id = user_id
        self.username = username

    def setType(self, type: str):
        self.type = type

    def to_dict(self) -> dict:
        result: dict = {}
        result["_raw"] = from_str(self.raw)
        result["content"] = from_union([from_str, from_none], self.content)
        result["created_at"] = from_union([to_float, from_none], self.created_at)
        result["hostname"] = from_union([from_str, from_none], self.hostname)
        result["ip"] = from_union([from_str, from_none], self.ip)
        result["originating_id"] = from_union([from_str, from_none], self.originating_id)
        result["parse_time"] = from_union([to_float, from_none], self.parse_time)
        result["path"] = from_str(self.path)
        result["producer"] = from_str(self.producer)
        result["relationships"] = from_union([lambda x: from_list(from_str, x), from_none], self.relationships)
        result["statistics.followers"] = from_union([to_float, from_none], self.statistics_followers)
        result["statistics.interactions"] = from_union([to_float, from_none], self.statistics_interactions)
        result["statistics.negative"] = from_union([to_float, from_none], self.statistics_negative)
        result["statistics.positive"] = from_union([to_float, from_none], self.statistics_positive)
        result["statistics.republish"] = from_union([to_float, from_none], self.statistics_republish)
        result["statistics.views"] = from_union([to_float, from_none], self.statistics_views)
        result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        result["type"] = from_str(self.type)
        result["user_id"] = from_union([from_str, from_none], self.user_id)
        result["username"] = from_union([from_str, from_none], self.username)
        return result