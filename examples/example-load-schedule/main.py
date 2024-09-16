import datetime
import os

from schedule_kspc import __desc__
from schedule_kspc import __author__
from schedule_kspc import __version__

from schedule_kspc import Store
from schedule_kspc import DirManager
from schedule_kspc import WebRequests
from schedule_kspc import ExcelParser
from schedule_kspc import JsonAdapter


DIR_ROOT: tuple = (
    'Расписание-EXCEL',
    'Расписание-JSON'
)

DIR_DEPARTMENT: tuple = (
    'Учебный корпус №1',
    'Учебный корпус №2',
    'Учебный корпус №3',
    'Филиал в г. Курчатов',
)


def tree_directories(root_name: str, node_names: tuple[str] = tuple()) -> DirManager.Tree:
    # Directory tree
    tree = DirManager.Tree(DirManager.Node(name=root_name, path=os.getcwd()))

    # Add node
    for department in node_names:
        tree.add_node(root=tree.root_node, name=department)

    # Make folders
    tree.make_folders(tree.root_node)

    return tree


@WebRequests.http_request
async def schedule_download(directories: DirManager.Tree) -> None:
    # Find html pattern (get files)
    files: list[tuple[str, str, str, str, str]] = await WebRequests.http_find_html_pattern(
        url=Store.URL["site"],
        pattern=Store.URL_FILE_PATTERN
    )

    # Cycle for files
    for department_id, items in enumerate(files):

        # Validate file move to directory
        if department_id >= len(directories.root_node.children):
            break

        # Full necessary file information
        file = dict(
            url=Store.URL['file'] + items[0],
            path=directories.root_node.children[department_id].path,
            name=items[0],
            shortname=items[1],
            index=int(items[2]),
            time_create=items[3],
            date_create=items[4],
        )

        # Output filename
        file['name']: str = f"{file['date_create']}_{file['time_create']}_{file['shortname']}"

        # Download file
        await WebRequests.http_download_file(url=file['url'], folder=file['path'], filename=file['name'])


if __name__ == "__main__":
    # Create directory tree
    xl_directories = tree_directories(root_name=DIR_ROOT[0], node_names=DIR_DEPARTMENT)
    json_directories = tree_directories(root_name=DIR_ROOT[1], node_names=())

    # Download schedule
    schedule_download(directories=xl_directories)

    # Get  relevant files / ( 'Department', ['file1', 'file2', ...] )
    departments_files: dict = DirManager.get_relevant_files(
        dir_tree=xl_directories, dir_node=xl_directories.root_node
    )

    # Json adapter
    json_adapter = JsonAdapter(
        filename='{0}\\{1}_schedule.json'.format(
            json_directories.root_node.path,
            datetime.datetime.now().strftime(Store.DATETIME_PATTERN)
        )
    )

    # Json write / create file & write data
    json_adapter.write(
        data={
            'info': {
                'version': __version__,
                'author': __author__,
                'desc': __desc__,
            }
        },
        indent=4, ensure_ascii=False
    )

    # id: int, department: str, files: list
    for department_id, (department_name, files) in enumerate(departments_files.items()):
        most_relevant_file: str = files[0]

        # Not found files (files[0] - first relevant file by datetime)
        if most_relevant_file is None:
            continue

        # File path / node path + relevant filename
        file_path: str = f'{xl_directories.root_node.children[department_id].path}\\{most_relevant_file}'

        # Excel parser
        xl_parser = ExcelParser(filename=file_path)

        # Json adapter
        json_adapter.append(
            data={
                department_name: {
                    'id': department_id,
                    'filename': most_relevant_file,
                    'file_datetime': datetime.datetime.now().strftime(Store.DATETIME_PATTERN),
                    'sheetnames': xl_parser.parse_sheetnames(),
                    'teachers': list(xl_parser.parse_teachers()),
                    'groupnames': xl_parser.parse_groups(values_only=True),
                    'sheetnames_days_and_groups': xl_parser.parse_sheetnames_days_and_groups(values_only=True),
                    'schedule_sheetnames': xl_parser.parse_schedule_sheetnames(),
                    'schedule_teachers': xl_parser.parse_schedule_teachers(),
                }
            },
            indent=4, ensure_ascii=False
        )
