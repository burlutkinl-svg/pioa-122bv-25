from db.backend.file import FileDatabase
from db.backend.memory import MemoryDatabase
from db.backend.errors import (
    TableAlreadyExistsError,
    TableNotFoundError,
    MissingColumnError,
    UnknownColumnError,
    InvalidStorageDataError,
    DatabaseError,
)


class TUI:
    def __init__(self) -> None:
        print("Выберите тип базы данных:")
        print("1. In-memory")
        print("2. File database")

        choice = input("Введите номер: ").strip()
        if choice == "2":
            self.database = FileDatabase()
        else:
            self.database = MemoryDatabase()

    def run(self):
        while True:
            print("\nДоступные команды: create_table, insert, select, exit")
            cmd = input("> ").strip()
            if cmd == "exit":
                break
            elif cmd == "create_table":
                name = input("Имя таблицы: ")
                cols = input("Колонки через пробел: ").split()
                try:
                    self.database.create_table(name, tuple(cols))
                    print(f"Таблица {name} создана.")
                except TableAlreadyExistsError as e:
                    print(f"Ошибка: {e}")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")
            elif cmd == "insert":
                name = input("Имя таблицы: ")
                record = {}
                parts = input("Поля (ключ=значение через пробел): ").split()
                for p in parts:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        try:
                            v = int(v)
                        except ValueError:
                            pass
                        record[k] = v
                try:
                    self.database.insert_record(name, record)
                    print("Запись добавлена.")
                except (TableNotFoundError, MissingColumnError, UnknownColumnError) as e:
                    print(f"Ошибка: {e}")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")
            elif cmd == "select":
                name = input("Имя таблицы: ")
                filters = {}
                filt_str = input("Фильтры (ключ=значение через пробел, пусто для всех): ")
                if filt_str:
                    for p in filt_str.split():
                        if '=' in p:
                            k, v = p.split('=', 1)
                            try:
                                v = int(v)
                            except ValueError:
                                pass
                            filters[k] = v
                try:
                    records = self.database.select_records(name, **filters)
                    for r in records:
                        print(r)
                except TableNotFoundError as e:
                    print(f"Ошибка: {e}")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")
            else:
                print("Неизвестная команда.")
