# schedule-kspc
Python библиотека, реализует автоматизированное расписание для Курского Государственного Политехнического Колледжа (КГПК).
KSPS - Kursk State Polytechnic College.

- Установка последней версии модуля
```console
pip install schedule-kspc
```

<h2> 📂 DirManager </h2>

<h3>Упрощенная работа с файлами и директориями:</h3>

- Бинарное дерево
- [Пример](https://github.com/bonkibon-education/schedule-kspc/tree/main/examples/example-dirmanager)

```python
import os
from schedule_kspc.DirManager import Tree, Node

if __name__ == '__main__':
    # Create root node/tree
    root_node = Node(name='root', path=os.getcwd())
    dir_manger = Tree(root_node=root_node)

    # Add node/child
    dir_manger.add_node(root=root_node, name='child-1')
    dir_manger.root_node.children[0].add_child(name='child-1-1')
    
    # Add node/child
    dir_manger.add_node(root=root_node, name='child-2')
    dir_manger.root_node.children[1].add_child(name='child-2-1')
    
    # Create folders
    dir_manger.make_folders(node=root_node)
    
    print(dir_manger)
```

- <h4>Файловая структура:</h4>

```console
root
├── child-1
│   └── child-1-1
└── child-2
    └── child-2-1

```


<h3>Поиск релевантных файлов из выбранного каталога</h3>

- Выявление паттерна даты и упорядочивание по хронологической близости

```python
import os
from random import randint
from datetime import datetime
from schedule_kspc.Store import DATETIME_PATTERN
from schedule_kspc.DirManager import Tree, Node, get_relevant_files

# Create file (random filename by datetime)
def create_file(path: str) -> None:

    year, month, day = (
        randint(2000, 2024),
        randint(1, 12),
        randint(1, 28)
    )

    hour, minute, second = (
        randint(0, 23),
        randint(0, 59),
        randint(0, 59)
    )

    random_date: datetime = datetime(year, month, day, hour, minute, second)
    filename: str = random_date.strftime(DATETIME_PATTERN)
    file = open(f'{path}\\{filename}_schedule.txt', mode='w')
    file.close()

# Create directory tree
def create_test_directory_tree() -> Tree:
    root_node = Node(name='root', path=os.getcwd())
    dir_manger = Tree(root_node=root_node)
    dir_manger.make_folders(node=root_node)
    return dir_manger


if __name__ == '__main__':
    # Directory tree
    tree = create_test_directory_tree()

    # Test files
    create_file(path=tree.root_node.path)
    create_file(path=tree.root_node.path)
    create_file(path=tree.root_node.path)
    create_file(path=tree.root_node.path)

    # Get all files in directory
    print(tree.get_files(tree.root_node))

    # Get relevant files
    print(get_relevant_files(dir_tree=tree, dir_node=tree.root_node))

```

- <h4>Файловая структура:</h4>

```console
  root:
  ├── 03.08.2012_10.07.20_schedule.txt
  ├── 13.07.2011_21.30.13_schedule.txt
  ├── 16.04.2023_13.20.12_schedule.txt
  └── 17.11.2006_05.21.10_schedule.txt
```

- <h4>Результат (Get all files in directory):</h4>

```console
  ['03.08.2012_10.07.20_schedule.txt', '13.07.2011_21.30.13_schedule.txt', '16.04.2023_13.20.12_schedule.txt', '17.11.2006_05.21.10_schedule.txt']
```

- <h4>Результат (Get relevant files):</h4>
  
```console
  {'root': ['16.04.2023_13.20.12_schedule.txt', '03.08.2012_10.07.20_schedule.txt', '13.07.2011_21.30.13_schedule.txt', '17.11.2006_05.21.10_schedule.txt']}
```


<h2>🌐 WebRequests</h2>

<h3>Упрощенная работа с асинхронными http запросами</h3>

- Поиск паттерна ссылки на html странице:
```python
from schedule_kspc import Store
from schedule_kspc import WebRequests


@WebRequests.http_request
async def get_files():
    files: list = await WebRequests.http_find_html_pattern(url=Store.URL["site"], pattern=Store.URL_FILE_PATTERN)
    print(files)

if __name__ == "__main__":
    get_files()

```

- Скачивание файлов по ссылке с указанием директории и названия файла  ([Пример](https://github.com/bonkibon-education/schedule-kspc/tree/main/examples/example-schedule-download))
```python
from os import getcwd
from schedule_kspc import Store
from schedule_kspc import WebRequests


current_path: str = getcwd()


@WebRequests.http_request
async def download_files():
    files: list = await WebRequests.http_find_html_pattern(url=Store.URL["site"], pattern=Store.URL_FILE_PATTERN)

    for file in files:
        await WebRequests.http_download_file(url=Store.URL['file'] + file[0], folder=current_path, filename=file[1])


if __name__ == "__main__":
    download_files()
```

<h2> 📅 ExcelParser </h2>

<h3>Автоматизированное чтение excel расписания</h3>

- [Пример](https://github.com/bonkibon-education/schedule-kspc/tree/main/examples/example-schedule-xlparser)

```python
from schedule_kspc import ExcelParser
from schedule_kspc.Store import WEEKDAYS, LESSONS, Lesson

if __name__ == '__main__':
    # Excel parser
    xl_parser = ExcelParser(filename='example.xlsx')

    # Parse schedule of sheetnames
    schedule: dict = xl_parser.parse_schedule_sheetnames()

    # Parse schedule of teachers
    schedule_teachers: dict = xl_parser.parse_schedule_teachers()

    ...
```

<h2> 📝 JsonAdapter </h2>

<h3>Автоматизированная запись данных в json файл</h3>

- [Пример](https://github.com/bonkibon-education/schedule-kspc/tree/main/examples/example-json-adapter)

```python
from schedule_kspc import JsonAdapter

if __name__ == '__main__':
    # Json adapter
    json_adapter = JsonAdapter(filename='file.json')

    # Json adapter / create file & write data
    json_adapter.write(
        data={'example': [1, 2, 3, 4, 5], 'example-2': 'string', 'example-3': dict(example='string')},
        indent=4, ensure_ascii=False
    )
```

- <h4>Результат:</h4>

```console
  file.json:
  {
      "example": [1, 2, 3, 4, 5],
      "example-2": "string",
      "example-3": {
          "example": "string"
      }
  }
```


<h2> ⚡ LoadSchedule </h2>

- Загрузка расписания, парсинг excel документа, сериализация в json файл:
  - [Пример](https://github.com/bonkibon-education/schedule-kspc/tree/main/examples/example-load-schedule)

