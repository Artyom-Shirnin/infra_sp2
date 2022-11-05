from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet)
from api.views import (UsersViewSet, user_create_view,
                       user_jwt_token_create_view)

router_version_1 = routers.DefaultRouter()
router_version_1.register('users', UsersViewSet, basename='users')
router_version_1.register('categories', CategoryViewSet,
                          basename='categories')
router_version_1.register('genres', GenreViewSet, basename='genres')
router_version_1.register('titles', TitleViewSet, basename='titles')
router_version_1.register(r'titles/(?P<title_id>\d+)/reviews',
                          ReviewViewSet, basename='reviews')
router_version_1.register(r'titles/(?P<title_id>\d+)/reviews'
                          r'/(?P<review_id>\d+)/comments',
                          CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_version_1.urls)),
    path('v1/auth/signup/', user_create_view),
    path('v1/auth/token/', user_jwt_token_create_view)
]
