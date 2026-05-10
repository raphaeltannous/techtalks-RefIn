import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from models.message import Message
from models.notification import NotificationPublic, NotificationsPublic
from models.user import User
from routers.dependencies import get_current_user, get_notification_service
from services.notification import NotificationService

router = APIRouter(
    tags=["notification"],
)


@router.get(
    "/",
    response_model=NotificationsPublic,
)
def get_all(
    *,
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(get_current_user)],
    offset: int = 0,
    limit: int = 25,
) -> Any:
    """
    Get all notifications for the current user.
    """
    return notification_service.get_all_by_user(
        user=user,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationPublic,
)
def get_by_id(
    *,
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(get_current_user)],
    notification_id: uuid.UUID,
) -> Any:
    """
    Get a notification by id.
    """
    return notification_service.get_by_id(
        user=user,
        notification_id=notification_id,
    )


@router.put(
    "/{notification_id}/seen",
    response_model=NotificationPublic,
)
def mark_as_seen(
    *,
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(get_current_user)],
    notification_id: uuid.UUID,
) -> Any:
    """
    Mark a notification as seen.
    """
    return notification_service.mark_as_seen(
        user=user,
        notification_id=notification_id,
    )


@router.delete(
    "/{notification_id}",
    response_model=Message,
)
def delete(
    *,
    notification_service: Annotated[
        NotificationService, Depends(get_notification_service)
    ],
    user: Annotated[User, Depends(get_current_user)],
    notification_id: uuid.UUID,
) -> Any:
    """
    Delete a notification.
    """
    notification_service.delete(
        user=user,
        notification_id=notification_id,
    )
    return Message(
        message="Notification deleted.",
    )
