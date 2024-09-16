from schedule_kspc import ExcelParser
from schedule_kspc import JsonAdapter


if __name__ == '__main__':
    # Excel parser
    xl_parser = ExcelParser(filename='example.xlsx')

    # Parse schedule of sheetnames
    schedule: dict = xl_parser.parse_schedule_sheetnames()

    # Parse schedule of teachers
    schedule_teachers: dict = xl_parser.parse_schedule_teachers()

    # Json adapter
    json_adapter = JsonAdapter(filename='schedule.json')

    # Json adapter / create file & write data
    json_adapter.write(
        data={
            'sheetnames': xl_parser.parse_sheetnames(),
            'teachers': list(xl_parser.parse_teachers()),
            'groupnames': xl_parser.parse_groups(values_only=True),
            'sheetnames_days_and_groups': xl_parser.parse_sheetnames_days_and_groups(values_only=True),
            'schedule_sheetnames': xl_parser.parse_schedule_sheetnames(),
            'schedule_teachers': xl_parser.parse_schedule_teachers(),
        },
        indent=4, ensure_ascii=False
    )
