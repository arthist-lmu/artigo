from .user import (
    CustomLoginView as LoginView,
    CustomLogoutView as LogoutView,
    CustomRegisterView as RegisterView,
    CustomUserDetailsView as UserDetailsView,
    CustomPasswordResetView as PasswordResetView,
    CustomPasswordResetConfirmView as PasswordResetConfirmView,
    CustomPasswordChangeView as PasswordChangeView,
)
from .resource import ResourceView
from .search import SearchView
from .reconcile import (
    ReconcileView,
    ReconcileAddView,
    ReconcileRemoveView,
)
from .game import GameView
from .highscore import HighscoreView
