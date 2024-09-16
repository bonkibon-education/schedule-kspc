from schedule_kspc import ExcelParser
from schedule_kspc.Store import WEEKDAYS, LESSONS, Lesson

if __name__ == '__main__':
    # Excel parser
    xl_parser = ExcelParser(filename='example.xlsx')

    # Parse schedule of sheetnames
    schedule: dict = xl_parser.parse_schedule_sheetnames()

    # Parse schedule of teachers
    schedule_teachers: dict = xl_parser.parse_schedule_teachers()

    print('\n[1] SHEETNAMES:\n - ', schedule.keys())
    for i, sheet in enumerate(schedule.keys()):
        print(f"\t{i + 1}) {sheet};")

    print('\n[2] GROUPS:')
    for i, sheet in enumerate(schedule.keys()):
        for group in schedule[sheet]:
            print(f"\t{i + 1}) {group}: {schedule[sheet][group]};")

    print('\n[3] SCHEDULE:')
    for i, sheet in enumerate(schedule.keys()):
        print(f"\t[{i + 1}]: {sheet} / {schedule[sheet]}")

        for j, group in enumerate(schedule[sheet]):
            print(f"\t\t[{j + 1}]: {group}")

            for weekday in range(len(schedule[sheet][group])):
                print(f"\t\t\t[{WEEKDAYS[weekday]}]:")
                for lesson in range(len(schedule[sheet][group][weekday])):
                    name: str = schedule[sheet][group][weekday][lesson][Lesson.LESSON_NAME.value]
                    teachers: tuple = schedule[sheet][group][weekday][lesson][Lesson.TEACHER.value]
                    cabinet: str = schedule[sheet][group][weekday][lesson][Lesson.CABINET.value]

                    print(
                        f"\t\t\t\t[{LESSONS[lesson]}]: "
                        f" {name}"
                        f" | {teachers}"
                        f" | {cabinet}"
                    )

    print('\n[4] TEACHERS:')
    for i, teacher in enumerate(schedule_teachers.keys()):
        print(f"\t[{teacher}]:")
        for weekday in range(len(schedule_teachers[teacher])):
            print(f"\t\t[{WEEKDAYS[weekday]}]:")
            for lesson in range(len(schedule_teachers[teacher][weekday])):
                name: str = schedule_teachers[teacher][weekday][lesson][Lesson.LESSON_NAME.value]
                teachers: tuple = schedule_teachers[teacher][weekday][lesson][Lesson.TEACHER.value]
                cabinet: str = schedule_teachers[teacher][weekday][lesson][Lesson.CABINET.value]
                group: str = schedule_teachers[teacher][weekday][lesson][Lesson.GROUP.value]

                print(
                    f"\t\t\t[{LESSONS[lesson]}]: "
                    f" {name}"
                    f" | {teachers}"
                    f" | {cabinet}"
                    f" | {group}"
                )
