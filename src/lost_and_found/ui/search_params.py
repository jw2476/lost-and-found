from .widgets import (
    HorizontalListViewModel,
    EntryViewModel,
    LabelViewModel,
    OptionMenuViewModel,
)
from ..state import SearchParamsModel, Category


class SearchParamsViewModel(HorizontalListViewModel):
    def __init__(self, search_params: SearchParamsModel) -> None:
        super().__init__(
            LabelViewModel("Name:"),
            EntryViewModel(search_params.name),
            LabelViewModel("Category:"),
            OptionMenuViewModel(
                search_params.category,
                lambda category: category.value if category else "All",
                *(None, *[category for category in Category]),
            ),
        )
