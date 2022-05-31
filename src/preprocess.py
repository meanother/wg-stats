"""Preprocessing raw data"""
import os
import re
import subprocess
from datetime import datetime


def run_shell_cmd(cmd: str) -> str:
    """run shel cmd"""
    result = subprocess.Popen(
        cmd.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=0,
    )
    stdout, stderr = result.communicate()
    return stdout[:-1]


def size_gb(num: str) -> float:
    """convert bytes to GB"""
    return round(int(num) / 1024 / 1024 / 1024, 3)


def get_dt() -> str:
    """return now dt"""
    return datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def to_datetime(timestamp: int) -> str:
    """convert unixtime to %Y-%m-%d %H:%M:%S"""
    return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")


def get_ip(string: str):
    """parse raw ip address to x.x.x.x"""
    pat = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    return pat.search(string).group()


def convert_list_to_dict(item: list) -> dict:
    """convert str to key:value"""
    result = {
        "interface": item[0],
        "peers": item[1],
        "preshared_keys": None if item[2] == "(none)" else item[2],
        "endpoints": item[3],
        "ip_address": get_ip(item[3]),
        "allowed_ips": item[4],
        "latest_handshakes": to_datetime(item[5]),
        "transfer_receiver": size_gb(item[6]),
        "transfer_sender": size_gb(item[7]),
        "persistent_keepalive": item[8],
        "event_ts": get_dt(),
    }
    return result


def convert_output(result: str) -> list:
    """convert str from wg show all dump to List[Dict]"""
    result_list = []
    prepare = result.split("\n")
    # header = prepare[0].split("\t")
    data = [i.split("\t") for i in prepare[1:]]
    for row in data:
        result_list.append(convert_list_to_dict(row))
    return result_list


def read_wg0() -> list:
    """parse wg0.conf file"""
    result_list = []
    with open("/etc/wireguard/wg0.conf", "r", encoding="utf-8") as file:
        raw = file.read()
    for line in raw.split("\n\n")[1:-1]:
        peer = line.split("\n")
        peer_key = peer[1].split(" = ")[1]
        peer_ip = peer[2].split(" = ")[1]
        result_list.append({"peer_key": peer_key, "peer_ip": peer_ip, "event_ts": get_dt()})
    return result_list


def get_users(path: str) -> list:
    """get user list from LS path"""
    result_list = []
    for dir_name, xpath, files in os.walk(path):
        result_list = [file for file in files if "_publickey" in file]
    return result_list


def get_user_public_id(username: str) -> dict:
    """get file data wor username"""
    with open(f"/etc/wireguard/{username}", "r", encoding="utf-8") as file:
        key = file.read().strip()
    return {"username": username, "key": key, "event_ts": get_dt()}
