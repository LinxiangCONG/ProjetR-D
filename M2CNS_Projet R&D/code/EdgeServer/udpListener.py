import os
import socket
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

local_dir = "/home/www/html/hls"
cloud_url = "http://192.168.20.20:8080/hls"

def download_missing_files(file_name, local_dir, remote_url):
    local_path = os.path.join(local_dir, file_name)

    if os.path.exists(local_path):
        print(f"files is exited：{file_name}")
    else:
        print(f"files is not exited，downloading：{file_name}")
        # 使用 wget 下载文件
        download_url = f"{remote_url}/{file_name}"
        try:
            subprocess.run(["wget", "-q", "-P", local_dir, download_url], check=True)
            print(f"Downloaded：{file_name}")
        except subprocess.CalledProcessError as e:
            print(f"Fail to Download：{file_name}，错误：{e}")


def parallel_download(file_list, local_dir, remote_url, max_workers=5):
    """
    多线程并行下载
    """
    # 确保本地目录存在
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # 创建线程池并分发任务
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(download_missing_files, file_name, local_dir, remote_url)
            for file_name in file_list
        ]
        # 等待所有任务完成
        for future in futures:
            future.result()


def udp_listener(host="0.0.0.0", port=54321):
    """
    监听 UDP 数据包，并解析 JSON 数据
    """
    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    print(f"Listening for UDP packets on {host}:{port}...")

    while True:
        global json_data
        data, addr = sock.recvfrom(1024)  # 接收数据
        print(f"Received packet from {addr}")

        try:
            # 尝试解析 JSON 数据
            json_data = json.loads(data.decode('utf-8'))
            print(f"Parsed JSON data: {json_data}")

            parallel_download(json_data,local_dir,cloud_url)

        except json.JSONDecodeError:
            print("Failed to decode JSON data")







if __name__ == "__main__":
    udp_listener()