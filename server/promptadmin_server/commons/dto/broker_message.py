from typing import Optional, TypeVar, Generic, Any
from pydantic import BaseModel, Field
import uuid

T = TypeVar('T', bound=dict | BaseModel)


class BrokerMessage(BaseModel, Generic[T]):
    # Object for exchanging information between microservice.
    # Also, an object that the microservice should receive when exchanging with internal microservices

    # Generic field containing data sent by another microservice
    # The default is a dict, but you can specify pydantic model
    data: T

    # Meta-information:
    # Required for some features RabbitMq
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # The place where the task was sent
    destination: str
    # Queue where the task was sent
    group: str

    # Microservice name where the message was created
    departure: str
    departure_unique_id: int

    reply_response: bool = False

    # Unused variables, but may be needed in the future
    initiator: str = 'system'
    user_data: Optional[dict] = None


class BrokerResponse(BaseModel):
    reply_message_id: str
    data: Any
