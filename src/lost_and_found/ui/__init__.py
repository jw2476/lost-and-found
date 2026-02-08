from ..state import AppModel
from .widgets import VerticalListViewModel
from .items import ItemsViewModel
from .search_params import SearchParamsViewModel


class AppViewModel(VerticalListViewModel):
    def __init__(self, app: AppModel):
        super().__init__(
            SearchParamsViewModel(app.search_params),
            ItemsViewModel(app.items, app.search_params),
        )
