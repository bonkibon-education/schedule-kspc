import os

from schedule_kspc import Store
from schedule_kspc import WebRequests


@WebRequests.http_request
async def schedule_download() -> None:
    # Find html pattern (get files)
    files: list[tuple[str, str, str, str, str]] = await WebRequests.http_find_html_pattern(
        url=Store.URL["site"], pattern=Store.URL_FILE_PATTERN
    )

    # Path to current directory
    file_path: str = os.getcwd()

    for items in files:
        # Get "re" pattern of result
        file = dict(
            name=items[0],
            shortname=items[1],
            index=int(items[2]),
            time_create=items[3],
            date_create=items[4],
        )

        # URL of the file to download
        url: str = Store.URL['file'] + file['name']

        await WebRequests.http_download_file(
            url=url,
            folder=file_path,
            filename=f"{file['index']}_{file['time_create']}_{file['date_create']}_{file['shortname']}"
        )

if __name__ == '__main__':
    schedule_download()
