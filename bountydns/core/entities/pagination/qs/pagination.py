class PaginationQS:
    def __init__(
        self,
        page: int = 1,
        per_page: int = 20,
        sort_by: str = "id",
        sort_dir: str = "asc",
    ):
        self.page = page
        self.per_page = per_page
        self.sort_by = sort_by
        self.sort_dir = sort_dir
