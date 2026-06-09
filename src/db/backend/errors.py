class TableError(Exception):
    pass

class DuplicateTableError(TableError):
    pass

class TableNotFoundError(TableError):
    pass
