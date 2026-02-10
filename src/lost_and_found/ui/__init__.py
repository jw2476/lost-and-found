from ..state import AppModel
from .items import ItemsViewModel
from .search_params import SearchParamsViewModel
from .widgets import VerticalListViewModel


class AppViewModel(VerticalListViewModel):
    def __init__(self, app: AppModel):
        super().__init__(
            SearchParamsViewModel(app.search_params),
            ItemsViewModel(app.items, app.search_params),
        )
