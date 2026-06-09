from db.backend.file import FileDatabase
from db.backend.memory import MemoryDatabase


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
                self.database.create_table(name, tuple(cols))
                print(f"Таблица {name} создана.")
            elif cmd == "insert":
                name = input("Имя таблицы: ")
                record = {}
                # упрощённый ввод: ключ=значение через пробел
                parts = input("Поля (ключ=значение через пробел): ").split()
                for p in parts:
                    if '=' in p:
                        k, v = p.split('=', 1)
                        try:
                            v = int(v)
                        except ValueError:
                            pass
                        record[k] = v
                self.database.insert_record(name, record)
                print("Запись добавлена.")
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
                records = self.database.select_records(name, **filters)
                for r in records:
                    print(r)
            else:
                print("Неизвестная команда.")
