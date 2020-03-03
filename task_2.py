import csv
import re
import datetime

if __name__ == '__main__':

    with open('test.csv') as test_file:
        test_csv = csv.DictReader(test_file, delimiter=';')
        rows_to_write = []

        for row in test_csv:

            row_is_correct = True
            try:
                i = int(row['id'])
                i = int(row['student_id'])
                i = int(row['class_id'])
                i = int(row['institution_id'])
                i = int(row['test_level_id'])
                i = int(row['licence_id'])
                if row['overall_score'] != '':
                    f = float(row['overall_score'])
                if row['confidence_level'] != '':
                    f = float(row['confidence_level'])
                if row['speaking_score'] != '':
                    f = float(row['speaking_score'])
                if row['writing_score'] != '':
                    f = float(row['writing_score'])
                if row['reading_score'] != '':
                    f = float(row['reading_score'])
                if row['listening_score'] != '':
                    f = float(row['listening_score'])
            except ValueError:
                row_is_correct = False
                print("INVALID ROW: ", row)

            if re.match(r"^(\d\d\.\d\d\.\d\d\s\d\d:\d\d)|()$", row['created_at']) is None:
                row_is_correct = False
                print("INVALID ROW: ", row)

            if re.match(r"^(\d\d\.\d\d\.\d\d\s\d\d:\d\d)|()$", row['updated_at']) is None:
                row_is_correct = False
                print("INVALID ROW: ", row)

            if row['last_event_time'] != '':
                last_event = re.sub('(\+\d\d)', '\g<1>:', row['last_event_time'])
                try:
                    datetime.datetime.fromisoformat(last_event)
                except ValueError:
                    row_is_correct = False
                    print("INVALID ROW: ", row)
            if row_is_correct:
                rows_to_write.append(row)

    with open('validated_test.csv', 'w', newline='') as validated_test_file:
        fieldnames = ['id', 'student_id', 'class_id', 'created_at', 'updated_at', 'last_event_time', 'overall_score',
                      'test_status', 'institution_id', 'authorized_at', 'confidence_level', 'speaking_score',
                      'writing_score', 'reading_score', 'listening_score', 'test_level_id', 'licence_id']
        writer = csv.DictWriter(validated_test_file, fieldnames=fieldnames, delimiter=';')
        writer.writerow({key: key for key in fieldnames})
        for row in rows_to_write:
            writer.writerow(row)

    with open('class.csv') as class_file:
        class_csv = csv.DictReader(class_file, delimiter=';')
        rows_to_write = []
        for row in class_csv:
            row_is_correct = True
            try:
                i = int(row['id'])
                i = int(row['institution_id'])
                i = int(row['owner_id'])
            except ValueError:
                row_is_correct = False

            if re.match(r"^[\x00-\x7F]+$", row['name']) is None:
                row_is_correct = False

            if re.match(r"^(\d\d\.\d\d\.\d\d\s\d\d:\d\d)|()$", row['created_at']) is None:
                row_is_correct = False

            if re.match(r"^(\d\d\.\d\d\.\d\d\s\d\d:\d\d)|()$", row['updated_at']) is None:
                row_is_correct = False

            if re.match(r"^(\d(\d)?(-\d(\d)?)?)|(15\+)|()$", row['teaching_hours']) is None:
                row_is_correct = False

            if re.match(r"^(\d\d\.\d\d\.\d\d\s\d\d:\d\d)|()$", row['latest_test_time']) is None:
                row_is_correct = False

            if re.match(r"[0-1]", row['has_student_with_scored_test']) is None:
                row_is_correct = False

            if row_is_correct:
                rows_to_write.append(row)

    with open('validated_class.csv', 'w', newline='') as validated_class_file:
        fieldnames = ['id', 'institution_id', 'owner_id', 'name', 'created_at', 'updated_at',
                      'teaching_hours', 'latest_test_time', 'has_student_with_scored_test']
        writer = csv.DictWriter(validated_class_file, fieldnames=fieldnames, delimiter=';')
        writer.writerow({key: key for key in fieldnames})
        for row in rows_to_write:
            writer.writerow(row)
