import os
import csv
import re
from src.main import user_input, resource_getter

action_list = [
    "Read head, prints out the n first lines of the resource",
    "Read tail, prints out the n last lines of the resource",
    "Display data, prints out all the data in a table"
]
encodings = ["utf-8", "iso-8859-1", "windows-1252"]
delimiter_choices = [';', ',', ':']


def print_actions():

    print("Available actions:")
    n = 0
    for action in action_list:
        n += 1
        print(str(n)+"- "+action)

def print_delimiter_choices():
    print("Available delimiter choices:")
    n = 0
    for choice in delimiter_choices:
        n += 1
        print(str(n)+"- "+choice)

def choose_action(url):
    action_input = user_input.get_int("Choose an action", 1, len(action_list), False)


    print(f"-You selected: {action_list[action_input - 1]}")

    n_lines = user_input.get_int("\nHow many lines to display", 1, None, True, )
    print("")

    if action_input == 1:
        print(read_head(url, n_lines))
    elif action_input == 2:
        read_tail(url, n_lines)
    elif action_input == 3:
        display_data_controller(url, n_lines)
    return

#Define functions for actions under

def read_head(url, n=5):
    text = ""
    if n is None or n == "":
        n = 5
    for encoding in encodings:
        try:
            with open(url, "r", encoding=encoding) as f:
                for i, line in enumerate(f):
                    if i >= n:
                        break
                    text += (line + "")
            text += f"(Used encoding: {encoding})"
            return text
        except UnicodeDecodeError:
            continue
    return "Couldn't read fil with normal encodings."

def read_tail(url, n=5, chunk_size=256):
    if n is None or n == "":
        n = 5
    n += 1
    try:
        with open(url, "rb") as f:
            f.seek(0, os.SEEK_END)
            pointer = f.tell()
            buffer = b""
            lines = []

            while pointer > 0 and len(lines) <= n:
                read_size = min(chunk_size, pointer)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size)
                buffer = chunk + buffer
                lines1 = buffer.split(b"\r")
                lines2 = buffer.split(b"\n")

                if len(str(lines1)) > len(str(lines2)):
                    lines = lines1
                else:
                    lines = lines2

                if pointer == 0:
                    break

            last_lines_bytes = lines[-n:] if len(lines) >= n else lines

            for encoding in encodings:
                try:
                    last_lines = [line.decode(encoding, errors="replace") for line in last_lines_bytes]
                    for line in last_lines:
                        print(line)

                    print(f"(Used encoding: {encoding})\n")
                    return
                except UnicodeDecodeError:
                    continue

            print("Couldn't read file with normal encodings.")

    except Exception as e:
        print(f"Error reading file: {e}")

def display_data_from_url(url, n=50):
    if n is None or n == "":
        n = 50



    for encoding in encodings:
        try:
            with open(url, "r", encoding=encoding) as f:
                reader = csv.reader(f, delimiter=';')
                headers = next(reader)
                col_widths = [max(len(h), 10) for h in headers]

                # print headers
                header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
                print(header_line)
                print("-" * len(header_line))

                for i, row in enumerate(reader):
                    if i >= n:
                        break
                    line = " | ".join(str(cell).rjust(w) + "   " for cell, w in zip(row, col_widths))
                    print(line)

            print(f"\n(Used encoding: {encoding})")
            return

        except UnicodeDecodeError:
            continue
    print("Couldn't read file with normal encodings.")

def display_data_controller(url, n_lines):
    guess_string = remove_last_line(read_head(url))
    recommended_delimiter, strength = resource_getter.get_delimiter(guess_string)
    rec_string = f"Recommended delimiter for this file is: {recommended_delimiter} Chance of correct: {strength}%. \nLeave blank to use recommended."
    print_delimiter_choices()

    delimiter_choice_int = user_input.get_int(rec_string, 1, len(delimiter_choices), True)
    if delimiter_choice_int is None:
        delimiter_choice = recommended_delimiter
    else:
        delimiter_choice = delimiter_choices[delimiter_choice_int-1]
    print(f"-You selected delimiter: {delimiter_choice}\n")

    data = read_url(url, delimiter_choice)
    if data is not None:
        data[1] = modify_date(data[0], data[1])
        display_data(data[1], data[0], data[2], n_lines)

def read_url(url, delimiter=';'):
    headers = None
    lines = []
    for encoding in encodings:
        try:
            with open(url, "r", encoding=encoding) as f:
                reader = csv.reader(f, delimiter=delimiter)
                headers = next(reader)

                for line in reader:
                    lines.append(line)

            return [headers, lines, encoding]

        except UnicodeDecodeError:
            continue
    print("Couldn't read file with normal encodings.")
    return None

def modify_date(headers, lines):
    possible_dato_headers = ["date", "dato"]
    headers_lower = [h.lower() for h in headers]
    index_date = 0
    pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')
    for possible in possible_dato_headers:
        if possible in headers_lower:
            index_date = headers_lower.index(possible)
            break
    else:
        return lines

    for line in lines:
        date = line[index_date]
        if bool(pattern.match(date)):
            line[index_date] = date[::-1]

    return lines

def display_data(lines, headers=None, encoding="", n=50):

    if n is None or n == "":
        n = 50


    if headers:
        from itertools import zip_longest
        col_widths = [
            max(len(str(h)), max(len(str(cell)) for cell in col if cell is not None), 10)
            for h, col in zip_longest(headers, zip(*lines), fillvalue="")
        ]
    else:
        col_widths = [max(len(str(cell)), 10) for cell in zip(*lines)]

    if headers:
        header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_line)
        print("-" * len(header_line))


    for line in lines:
        if n == 0:
            break
        row = " | ".join(str(cell).rjust(w) for cell, w in zip(line, col_widths))
        print(row)
        n -= 1

    if encoding != "":
        print(f"\n(Used encoding: {encoding})")

def remove_last_line(s):
    lines = s.splitlines()
    if not lines:
        return s
    return "\n".join(lines[:-1])





