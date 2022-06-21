import csv
question_path = "sample_data/question.csv"
answer_path = "sample_data/answer.csv"
question_keys = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_keys = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

def reader_csv(filename):
    dict_list = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict_list.append(row)
    return dict_list


def writer_csv(filename, fieldnames, new_data):
    with open(filename, 'a') as my_file:
        writer = csv.DictWriter(my_file, fieldnames=fieldnames)
        writer.writerow(new_data)

def write_data(dictionary, filename,):
    data = reader_csv(filename)

    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=answer_keys)
        writer.writeheader()

        for row in data:
            writer.writerow(row)
        writer.writerow(dictionary)