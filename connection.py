import csv


ANSWER_HEADER = ["id","submission_time","vote_number","question_id","message","image"]
QUESTION_HEADER = ["id","submission_time","view_number","vote_number","title","message","image"]


def read_data_from_file(file_name):
    with open(f"sample_data/{file_name}", 'r') as file:
        reader = csv.DictReader(file)
        stories = []
        for story in reader:
            stories.append(story)
        return stories


def write_data_to_file(file_name, data, data_header):
    with open(f"sample_data/{file_name}", 'w') as file:
        writer = csv.DictWriter(file, data_header)
        writer.writeheader()
        writer.writerows(data)


def add_data_to_file(file_name, data, data_header):
    with open(f"sample_data/{file_name}", 'a+') as file:
        writer = csv.DictWriter(file, data_header)
        writer.writerow(data)
