import os
import json
from db.backend.memory import Table
from db.backend.errors import TableNotFoundError

def get_names_set():
    if not os.path.exists("names.txt"):
        with open("names.txt", "w") as f:
            f.write("")
    with open("names.txt", "r") as f:
        content = f.read().strip()
        return set(content.split()) if content else set()

def save_names_set(names):
    with open("names.txt", "w") as f:
        f.write(" ".join(names))

def main():
    current_table = None
    head = "пустой базе данных"

    print("\n\nВведите 0 чтобы выйти.")
    print("Чтобы добавить новую базу данных введите create <имя>")
    print("Чтобы перейти в другую базу данных введите check <имя>")
    print("Чтобы удалить базу данных напишите destroy <имя>")
    print("Чтобы ввести данные напишите write")
    print("Чтобы прочитать данные введите read -filt <поля_которые_хотите_прочитать>")
    print("Чтобы удалить запись введите delete <записи_которые_нужно_удалить>")
    print("Чтобы отсортировать записи введите sort asc|desc|none\n")

    while True:
        x = input().strip()
        if x == "0":
            break

        if current_table is None:
            # ----- Нет выбранной базы данных -----
            if x.startswith("create "):
                parts = x.split()
                if len(parts) != 2:
                    print("Введите create <имя>")
                    continue
                name = parts[1]
                filename = f"{name}.json"
                if filename in get_names_set():
                    print(f"База данных {name} уже существует")
                    continue
                try:
                    with open(filename, 'x') as f:
                        json.dump({}, f)
                    names = get_names_set()
                    names.add(filename)
                    save_names_set(names)
                    print("База данных создана")
                    current_table = Table(name)
                    head = name
                except FileExistsError:
                    print(f"База данных {name} уже существует")
            elif x.startswith("check "):
                parts = x.split()
                if len(parts) != 2:
                    names = [n.replace('.json', '') for n in get_names_set()]
                    if names:
                        print(f"Существующие базы данных: {', '.join(names)}")
                    else:
                        print("Нету баз данных, создайте новую: create <имя>")
                    print(f"Сейчас вы находитесь в {head}")
                    continue
                name = parts[1]
                filename = f"{name}.json"
                if filename not in get_names_set():
                    print("Такой базы данных нет")
                    continue
                current_table = Table(name)
                head = name
                print(f"Вы перешли в {name}")
            elif x.startswith("destroy "):
                parts = x.split()
                if len(parts) != 2:
                    print("Введите destroy <имя>")
                    continue
                name = parts[1]
                filename = f"{name}.json"
                if filename not in get_names_set():
                    print(f"Базы данных {name} не существует")
                    continue
                os.remove(filename)
                names = get_names_set()
                names.remove(filename)
                save_names_set(names)
                print(f"База данных {name} уничтожена")
                if current_table and current_table.name == name:
                    current_table = None
                    head = "пустой базе данных"
            else:
                print("Вы не выбрали базу данных")
        else:
            # ----- База данных выбрана -----
            if x == "write":
                key = input("Введите название записи: ")
                content = input("Введите содержимое записи, в качестве разделителя используйте пробел: ")
                current_table.write(key, content)
                print("Запись добавлена")
            elif x.startswith("read"):
                filters = None
                if "-filt" in x:
                    try:
                        filters = x.split("-filt")[1].split()
                    except IndexError:
                        pass
                records = current_table.read(filters)
                if not records:
                    print("В базе данных нет записей")
                else:
                    for key, val in records.items():
                        print(f"{key}: {' '.join(val)}")
            elif x.startswith("delete"):
                keys = x.split()[1:]
                if not keys:
                    keys = input("Введите названия записей, которые хотите удалить: ").split()
                current_table.delete(keys)
                print("Записи удалены")
            elif x.startswith("create "):
                parts = x.split()
                if len(parts) != 2:
                    print("Введите create <имя>")
                    continue
                name = parts[1]
                filename = f"{name}.json"
                if filename in get_names_set():
                    print(f"База данных {name} уже существует")
                    continue
                with open(filename, 'x') as f:
                    json.dump({}, f)
                names = get_names_set()
                names.add(filename)
                save_names_set(names)
                print("База данных создана")
            elif x.startswith("check "):
                parts = x.split()
                if len(parts) != 2:
                    names = [n.replace('.json', '') for n in get_names_set()]
                    print(f"Существующие базы данных: {', '.join(names)}")
                    print(f"Сейчас вы находитесь в {current_table.name}")
                    continue
                name = parts[1]
                filename = f"{name}.json"
                if filename not in get_names_set():
                    print("Такой базы данных нет")
                    continue
                current_table = Table(name)
                head = name
                print(f"Вы перешли в {name}")
            elif x.startswith("destroy "):
                parts = x.split()
                if len(parts) != 2:
                    print("Введите destroy <имя>")
                    continue
                name = parts[1]
                filename = f"{name}.json"
                if filename not in get_names_set():
                    print(f"Базы данных {name} не существует")
                    continue
                os.remove(filename)
                names = get_names_set()
                names.remove(filename)
                save_names_set(names)
                print(f"База данных {name} уничтожена")
                if current_table.name == name:
                    current_table = None
                    head = "пустой базе данных"
            elif x.startswith("sort "):
                parts = x.split()
                if len(parts) != 2:
                    print("Используйте sort asc|desc|none")
                    continue
                order = parts[1].lower()
                if order in ('asc', 'desc', 'none'):
                    current_table.set_sort(order if order != 'none' else None)
                    print(f"Сортировка установлена: {order}")
                else:
                    print("Используйте sort asc|desc|none")
            else:
                print(f"Команда {x} не найдена")
