import ipaddress


def generate_and_save_ips(start_ip, end_ip, filename):
    start = int(ipaddress.IPv4Address(start_ip))
    end = int(ipaddress.IPv4Address(end_ip))
    count = 0
    with open(filename, "w") as f:
        for ip_int in range(start, end + 1):
            ip = str(ipaddress.IPv4Address(ip_int))
            f.write(ip + "\n")
            count += 1
    print(f"Сгенерировано IP: {count}")

    return count


# if __name__ == "__main__":
#     generate_and_save_ips("192.165.1.1", "192.168.1.10", "ips.txt")
