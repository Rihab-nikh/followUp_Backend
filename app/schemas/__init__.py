"""
Validation schemas package initialization
"""

from .user_schema import (
    UserSchema, UserUpdateSchema, UserLoginSchema, UserRegisterSchema,
    UserResponseSchema, PasswordChangeSchema, PasswordResetSchema,
    PasswordResetConfirmSchema, TokenRefreshSchema, UserPreferencesSchema
)

from .meeting_schema import (
    MeetingSchema, MeetingCreateSchema, MeetingUpdateSchema,
    MeetingStatusUpdateSchema, MeetingFilterSchema, MeetingResponseSchema,
    CalendarViewSchema
)

from .task_schema import (
    TaskSchema, TaskCreateSchema, TaskUpdateSchema, TaskStatusUpdateSchema,
    TaskFilterSchema, TaskResponseSchema, KanbanBoardSchema, TaskMoveSchema
)

from .notification_schema import (
    NotificationSchema, NotificationCreateSchema, NotificationResponseSchema,
    NotificationUpdateSchema, NotificationFilterSchema, BulkNotificationUpdateSchema
)

from .ai_chat_schema import (
    AIMessageSchema, AIChatSessionSchema, AIMessageCreateSchema,
    AIChatRequestSchema, AIChatResponseSchema, AIChatHistoryResponseSchema,
    AIMessageResponseSchema, AIChatSessionDeleteSchema
)

from .dashboard_schema import (
    KPIMetricSchema, DashboardKPIsSchema, ChartDataPointSchema,
    MeetingActivityChartSchema, RecentItemSchema, RecentMeetingsSchema,
    UpcomingTasksSchema, DashboardAnalyticsSchema, DateRangeSchema
)

__all__ = [
    # User schemas
    'UserSchema', 'UserUpdateSchema', 'UserLoginSchema', 'UserRegisterSchema',
    'UserResponseSchema', 'PasswordChangeSchema', 'PasswordResetSchema',
    'PasswordResetConfirmSchema', 'TokenRefreshSchema', 'UserPreferencesSchema',
    
    # Meeting schemas
    'MeetingSchema', 'MeetingCreateSchema', 'MeetingUpdateSchema',
    'MeetingStatusUpdateSchema', 'MeetingFilterSchema', 'MeetingResponseSchema',
    'CalendarViewSchema',
    
    # Task schemas
    'TaskSchema', 'TaskCreateSchema', 'TaskUpdateSchema', 'TaskStatusUpdateSchema',
    'TaskFilterSchema', 'TaskResponseSchema', 'KanbanBoardSchema', 'TaskMoveSchema',
    
    # Notification schemas
    'NotificationSchema', 'NotificationCreateSchema', 'NotificationResponseSchema',
    'NotificationUpdateSchema', 'NotificationFilterSchema', 'BulkNotificationUpdateSchema',
    
    # AI chat schemas
    'AIMessageSchema', 'AIChatSessionSchema', 'AIMessageCreateSchema',
    'AIChatRequestSchema', 'AIChatResponseSchema', 'AIChatHistoryResponseSchema',
    'AIMessageResponseSchema', 'AIChatSessionDeleteSchema',
    
    # Dashboard schemas
    'KPIMetricSchema', 'DashboardKPIsSchema', 'ChartDataPointSchema',
    'MeetingActivityChartSchema', 'RecentItemSchema', 'RecentMeetingsSchema',
    'UpcomingTasksSchema', 'DashboardAnalyticsSchema', 'DateRangeSchema'
]
