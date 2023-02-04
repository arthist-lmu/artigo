from .game import GameView
from .home import HomeView
from .reconcile import (
    ReconcileView,
    ReconcileAddView,
    ReconcileRemoveView,
)
from .collection import (
    CollectionView,
    CollectionAddView,
    CollectionRemoveView,
)
from .resource import ResourceView
from .search import SearchView
from .session import SessionView
from .sessions import SessionsView
from .statistics import (
    ScoresView,
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
