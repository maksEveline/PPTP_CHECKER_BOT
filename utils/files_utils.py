def clean_checked():
    with open("checked.txt", "w") as f:
        f.write("")


def get_count_checked():
    with open("checked.txt", "r") as f:
        lines = f.readlines()
    return len(lines)


def add_checked(ip):
    with open("checked.txt", "a") as f:
        f.write(ip + "\n")


def get_unique_lines(base_path, check_path):
    with open(base_path, "r", encoding="utf-8") as f:
        base_lines = set(line.strip() for line in f)
    with open(check_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]
