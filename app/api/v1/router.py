# app/api/v1/router.py

from fastapi import APIRouter

from .endpoints  import auth, users, posts, comments, files, ws

api_router = APIRouter()

# Authentication routes (/api/v1/auth)
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

# User routes (/api/v1/users)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

# Post routes (/api/v1/posts)
api_router.include_router(
    posts.router,
    prefix="/posts",
    tags=["Posts"],
)

# Comment & Reply routes
# - GET/POST    /api/v1/posts/{post_id}/comments
# - PUT/DELETE /api/v1/comments/{comment_id}
# - GET/POST    /api/v1/comments/{comment_id}/replies
api_router.include_router(
    comments.router,
    tags=["Comments"],
)

# File upload/download routes
# - POST /api/v1/posts/{post_id}/files
# - GET  /api/v1/files/{file_id}/download
# - DELETE /api/v1/files/{file_id}
api_router.include_router(
    files.router,
    tags=["Files"],
)

# WebSocket routes
api_router.include_router(
    ws.router,
    tags=["WebSocket"],
)
