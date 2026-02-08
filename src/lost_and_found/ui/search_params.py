from .widgets import HorizontalListViewModel, EntryViewModel, LabelViewModel
from ..state import SearchParamsModel


class SearchParamsViewModel(HorizontalListViewModel):
    def __init__(self, search_params: SearchParamsModel) -> None:
        super().__init__(
            LabelViewModel("Name:"),
            EntryViewModel(search_params.name),
        )
