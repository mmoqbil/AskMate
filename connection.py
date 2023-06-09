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

def delete_question(question_id):
    data = reader_csv(question_path)
    with open(question_path, "w") as file:
        writer = csv.DictWriter(file, question_keys)
        writer.writeheader()
        for row in data:
            if row["id"] != question_id:
                writer.writerow(row)
    return data

def delete_answer(answer_id):
    data = reader_csv(answer_path)
    with open(answer_path, "w") as file:
        writer = csv.DictWriter(file, answer_keys)
        writer.writeheader()

        for row in data:
            if row["id"] != answer_id:
                writer.writerow(row)
        return data

def update_question(new_line, question_id):
    data = reader_csv(question_path)

    with open(question_path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=question_keys)
        writer.writeheader()
        for question in data:
            if question["id"] == question_id:
                writer.writerow(new_line)
            else:
                writer.writerow(question)

    return data