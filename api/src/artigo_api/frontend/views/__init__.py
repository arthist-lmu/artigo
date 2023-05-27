from .api import (
    CustomSchemaView as SchemaView,
    CustomRedocView as RedocView,
    CustomSwaggerView as SwaggerView,
)
from .collection import (
    CollectionAddView,
    CollectionRemoveView,
    CollectionChangeView,
)
from .collections import CollectionsView
from .game import GameView
from .home import HomeView
from .reconcile import (
    ReconcileView,
    ReconcileAddView,
    ReconcileRemoveView,
)
from .resource import ResourceView
from .search import SearchView
from .session import SessionView
from .sessions import SessionsView
from .statistics import (
    StatisticsView,
)
from .user import (
    CustomLoginView as LoginView,
    CustomLogoutView as LogoutView,
    CustomRegisterView as RegisterView,
    CustomUserDetailsView as UserDetailsView,
    CustomPasswordResetView as PasswordResetView,
    CustomPasswordResetConfirmView as PasswordResetConfirmView,
    CustomPasswordChangeView as PasswordChangeView,
)
