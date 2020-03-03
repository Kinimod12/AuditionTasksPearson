import csv
import datetime
import re

if __name__ == "__main__":

    def create_db_connection():
        # Code here would depend on RDBMS used
        pass

    def create_tables():
        sql_dict = create_sql_dict()
        execute_sql_statement(sql_dict['create_utilization_table'])
        execute_sql_statement(['create_average_score_table'])


    def create_sql_dict():
        return {'insert_test_utilization': """INSERT INTO test_utilization (class_id, class_name, teaching_hours,
                                                                            test_id, test_created_at,
                                                                            test_authorized_at, test_level,
                                                                            class_test_number
                                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s}
                                            """,

                'insert_test_average_scores': """INSERT INTO test_average_scores (class_id, class_name, teaching_hours,
                                                                                  test_created_at, test_authorized_at,
                                                                                  avg_class_test_overall_score)
                                                 VALUES(%s, %s, %s, %s, %s, %s)
                                              """,

                'create_utilization_table': """CREATE TABLE IF NOT EXISTS test_utilization 
                                               (
                                                   class_id,
                                                   class_name,
                                                   teaching_hours,
                                                   test_id,
                                                   test_created_at,
                                                   test_authorized_at,
                                                   test_level,
                                                   class_test_number
                                               )
                                            """,

                'create_average_score_table': """CREATE TABLE IF NOT EXISTS test_average_score
                                                       (
                                                           class_id,
                                                           class_name,
                                                           teaching_hours,
                                                           test_created_at,
                                                           test_authorized_at,
                                                           avg_class_test_overall_score
                                                       )
                                               """
               }

    def execute_sql_statement(sql, data=''):
        # Code here would depend on RDBMS used
        pass

if __name__ == "__main__":

    create_db_connection()
    create_tables()
    sql_dictionary = create_sql_dict()

    with open('test_utilization.csv') as test_utilization_file:
        test_utilization_data = []
        test_utilization_csv = csv.reader(test_utilization_file, delimiter=';')
        for row in test_utilization_csv:
            test_utilization_data.append(row)

        del test_utilization_data[0]

        for row in test_utilization_data:
            row[4] = re.sub('\.', ' ', row[4])
            row[4] = re.sub(':', ' ', row[4])
            row[4] = datetime.datetime.strptime(row[4], '%d %m %y %H %M')
            row[5] = re.sub('\.', ' ', row[5])
            row[5] = re.sub(':', ' ', row[5])
            row[5] = datetime.datetime.strptime(row[5], '%d %m %y %H %M')
            row[7] = int(row[7])
            execute_sql_statement(sql_dictionary['insert_test_utilization'], row)

    with open('test_average_scores.csv') as test_average_file:
        test_average_data = []
        test_average_csv = csv.reader(test_average_file, delimiter=';')
        for row in test_average_csv:
            test_average_data.append(row)

        del test_average_data[0]

        for row in test_average_data:
            row[3] = re.sub('\.', ' ', row[3])
            row[3] = re.sub(':', ' ', row[3])
            row[3] = datetime.datetime.strptime(row[3], '%d %m %y %H %M')
            row[4] = re.sub('\.', ' ', row[4])
            row[4] = re.sub(':', ' ', row[4])
            row[4] = datetime.datetime.strptime(row[4], '%d %m %y %H %M')
            try:
                row[5] = float(row[5])
            except ValueError:
                row[5] = None
            execute_sql_statement(sql_dictionary['insert_test_average_scores'], row)
