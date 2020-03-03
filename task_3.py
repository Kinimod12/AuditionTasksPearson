import csv

if __name__ == "__main__":
    with open('validated_test.csv') as test_file:
        test_csv = csv.DictReader(test_file, delimiter=';')
        test_data = []
        for row in test_csv:
            if row['authorized_at'] != '':
                dict_row = {'test_id': row['id'], 'test_created_at': row['created_at'],
                            'test_authorized_at': row['authorized_at'],
                            'test_level': row['test_level_id'],
                            'class_id': int(row['class_id'])}
                test_data.append(dict_row)

    with open('validated_class.csv') as class_file:
        class_csv = csv.DictReader(class_file, delimiter=';')
        class_data = []
        for row in class_csv:
            dict_row = {'class_id': int(row['id']), 'class_name': row['name'],
                        'teaching_hours': row['teaching_hours']}
            class_data.append(dict_row)
        class_data = sorted(class_data, key=lambda k: ['class_id'])

    test_utilization_data = []

    test_utilization_data = []
    for class_row in class_data:
        class_test_number = 0
        for test_row in test_data:
            if class_row['class_id'] == test_row['class_id']:
                class_test_number += 1
                test_utilization_data.append({'class_id': class_row['class_id'],
                                              'class_name': class_row['class_name'],
                                              'teaching_hours': class_row['teaching_hours'],
                                              'test_id': test_row['test_id'],
                                              'test_created_at': test_row['test_created_at'],
                                              'test_authorized_at': test_row['test_authorized_at'],
                                              'test_level': test_row['test_level'],
                                              'class_test_number': class_test_number
                                              })

    test_utilization_data = sorted(test_utilization_data, key=lambda k: k['class_id'])

    with open('test_utilization.csv', 'w', newline='') as test_utilization_file:
        fieldnames = ['class_id', 'class_name', 'teaching_hours', 'test_id', 'test_created_at',
                      'test_authorized_at', 'test_level', 'class_test_number']
        writer = csv.DictWriter(test_utilization_file, fieldnames=fieldnames, delimiter=';')
        writer.writerow({key: key for key in fieldnames})

        for element in test_utilization_data:
            writer.writerow(element)
