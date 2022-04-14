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
    _raw: str
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

    def __init__(self, raw: str, type: str = None, path: str = None, content: Optional[str] = None, created_at: Optional[float] = None, hostname: Optional[str] = None, ip: Optional[str] = None, originating_id: Optional[str] = None, parse_time: Optional[float] = None,  producer: str = None, relationships: Optional[List[str]] = None, statistics_followers: Optional[float] = None, statistics_interactions: Optional[float] = None, statistics_negative: Optional[float] = None, statistics_positive: Optional[float] = None, statistics_republish: Optional[float] = None, statistics_views: Optional[float] = None, tags: Optional[List[str]] = None, user_id: Optional[str] = None, username: Optional[str] = None) -> None:
        self._raw = raw
        self.content = content
        self.hostname = hostname
        self.ip = ip
        self.originating_id = originating_id
        if (parse_time):
            self.parse_time = parse_time
        else:
            self.parse_time = int(time.time())
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
        return  {k: v for k, v in self.__dict__.items() if type(v) is not None}