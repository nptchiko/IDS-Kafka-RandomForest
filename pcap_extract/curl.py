import subprocess
import time
import random


unsafe_urls = [
    "https://client-cert-missing.badssl.com/",
    "https://3des.badssl.com/",
    "http://http-login.badssl.com/submit/"
]


safe_urls = [
    "https://sha256.badssl.com/",
    "https://sha384.badssl.com/",
    "https://sha512.badssl.com/",
    "https://rsa2048.badssl.com/",
    "https://hsts.badssl.com/",
    "https://mozilla-modern.badssl.com/",
    "https://ecc256.badssl.com/",
    "https://tls-v1-2.badssl.com:1012/",
    "https://tls-v1-3.badssl.com:1013/"
]


all_urls = unsafe_urls * 3 + safe_urls


end_time = time.time() + 50 * 60

while time.time() < end_time:
    url = random.choice(all_urls)
    referer = "https://badssl.com/"

    # Nếu là HTTP POST, gửi dữ liệu giả lập đăng nhập
    if "http-login.badssl.com" in url:
        command = f'curl -X POST "{url}" --data "username=test&password=1234"'
    else:
        command = f'curl -L "{url}" -H "Referer: {referer}"'

    print(f"[+] Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)




    time.sleep(random.randint(10, 30))
