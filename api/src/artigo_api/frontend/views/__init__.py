from .collection import CollectionView
from .resource import ResourceView
from .search import SearchView
from .game_rest_views import TaggingView, GametypeView, TagView, GameResourceView, GamesessionView, \
    GameroundView, TabooTagsView, \
    GameResourceViewPicture, ARTigoGameView, TagATagGameView, ARTigoTabooGameView, CombinoGameView
from .user import get_csrf_token, UserView#, LoginView, LogoutView, RegisterView
