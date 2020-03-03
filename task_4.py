import csv

if __name__ == "__main__":
    with open('validated_test.csv') as test_file:
        test_csv = csv.DictReader(test_file, delimiter=';')
        test_data = []

        for row in test_csv:
            if row['authorized_at'] != '' and row['test_status'] == 'SCORING_SCORED' and row['overall_score'] != '':
                dict_row = {'test_id': row['id'], 'test_created_at': row['created_at'],
                            'test_authorized_at': row['authorized_at'],
                            'test_overall_score': float(row['overall_score']),
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

    average_scores_data = []
    for class_row in class_data:
        class_test_number = 0
        sum_of_scores = 0
        for test_row in test_data:
            if test_row['class_id'] == class_row['class_id']:
                class_test_number += 1
                test_creation_time = test_row['test_created_at']
                test_authorization_time = test_row['test_authorized_at']
                sum_of_scores += test_row['test_overall_score']

        if class_test_number > 0:
            average_score = sum_of_scores / class_test_number
        else:
            average_score = "N/A"

        average_scores_data.append({'class_id': class_row['class_id'], 'class_name': class_row['class_name'],
                                    'teaching_hours': class_row['teaching_hours'],
                                    'test_created_at': test_creation_time,
                                    'test_authorized_at': test_authorization_time,
                                    'avg_class_test_overall_score': average_score
                                    })
    with open('test_average_scores.csv', 'w', newline='') as test_average_file:
        fieldnames = ['class_id', 'class_name', 'teaching_hours', 'test_created_at',
                      'test_authorized_at', 'avg_class_test_overall_score']
        writer = csv.DictWriter(test_average_file, fieldnames=fieldnames, delimiter=';')
        writer.writerow({key: key for key in fieldnames})

        for element in average_scores_data:
            writer.writerow(element)
