from dataclasses import dataclass

@dataclass
class SendMessage:
    type = "SendMessage"
    phone: str
    message: str

@dataclass
class RecommendationMessage:
    type = "RecommendationMessage"
    phone: str
    caption: str
    base64: str
    
