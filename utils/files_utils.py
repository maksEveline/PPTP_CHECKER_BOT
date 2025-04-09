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
