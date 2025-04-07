import pyshark
import subprocess
import pandas as pd
import re
import binascii
import numpy as np
import logging
from concurrent.futures import ThreadPoolExecutor
import os
from typing import Dict, List, Optional, Tuple, Any


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


PCAP_FILE = "badssl2.pcap"
CSV_FILE = "dataset.csv"
OPENSSL_PATH = r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"
TIMEOUT = 5

def get_certificate_info(server_name: str) -> Dict[str, str]:
    """Lấy thông tin chứng chỉ SSL từ server sử dụng OpenSSL."""
    if not server_name or server_name == "Unknown":
        return {
            "cipher_suite": "Unknown",
            "unstrusted_cert": "Unknown",
            "expire_certificate": "Unknown"
        }

    try:
        if not os.path.exists(OPENSSL_PATH):
            logger.warning(f"OpenSSL không tìm thấy tại: {OPENSSL_PATH}")
            return {
                "cipher_suite": "OpenSSL not found",
                "unstrusted_cert": "Unknown",
                "expire_certificate": "Unknown"
            }

        cmd = [
            OPENSSL_PATH,
            "s_client", "-connect", f"{server_name}:443",
            "-servername", server_name
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
            # timeout=TIMEOUT
        )

        output = result.stdout


        info = {
            "cipher_suite": "Unknown",
            "unstrusted_cert": "No",
            "expire_certificate": "Valid"
        }

        if output:

            cipher_match = re.search(r"Cipher\s*:\s*(.+)", output)
            if cipher_match:
                info["cipher_suite"] = cipher_match.group(1)


            if "self-signed certificate" in output or "self-signed certificate in certificate chain" in output:
                info["unstrusted_cert"] = "Yes"


            if "certificate has expired" in output:
                info["expire_certificate"] = "Expired"

        return info

    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout khi kết nối đến {server_name}")
        return {
            "cipher_suite": "Timeout",
            "unstrusted_cert": "Unknown",
            "expire_certificate": "Unknown"
        }
    except Exception as e:
        logger.error(f"Lỗi khi lấy thông tin chứng chỉ cho {server_name}: {str(e)}")
        return {
            "cipher_suite": f"Error: {str(e)[:50]}",
            "unstrusted_cert": "Unknown",
            "expire_certificate": "Unknown"
        }

def process_packet(pkt: Any) -> Optional[List[Any]]:

    try:
        # Khởi tạo giá trị mặc định
        packet_data = {
            "protocol": None,
            "host": None,
            "url": None,
            "method": None,
            "content_type": None,
            "sensitive_data": None,
            "server_name": None,
            "cipher_suite": None,
            "issuer": None,
            "subject": None,
            "unstrusted_cert": None,
            "tls_version": None,
            "expire_certificate": None,
            "hsts": None
        }

        # Xử lý HTTP
        if "HTTP" in pkt:
            packet_data["protocol"] = "HTTP"
            packet_data["host"] = getattr(pkt.http, "host", "N/A")
            packet_data["url"] = getattr(pkt.http, "request_uri", "N/A")
            packet_data["method"] = getattr(pkt.http, "request_method", "N/A")
            packet_data["content_type"] = getattr(pkt.http, "content_type", "N/A")

            # Kiểm tra HSTS (Strict-Transport-Security)
            packet_data["hsts"] = "No"
            if hasattr(pkt.http, "response_for_uri") and hasattr(pkt.http, "response_line"):
                headers = getattr(pkt.http, "response_line", "")
                if "Strict-Transport-Security" in headers:
                    packet_data["hsts"] = "Yes"

            # Kiểm tra dữ liệu nhạy cảm
            if packet_data["content_type"] == "application/x-www-form-urlencoded" and hasattr(pkt.http, "file_data"):
                try:
                    hex_data = pkt.http.file_data.replace(":", "")
                    packet_data["sensitive_data"] = binascii.unhexlify(hex_data).decode('utf-8', errors='ignore')
                except Exception as e:
                    packet_data["sensitive_data"] = f"Decode Error: {str(e)[:50]}"

        # Xử lý TLS
        elif "TLS" in pkt:
            packet_data["protocol"] = "TLS"
            packet_data["server_name"] = getattr(pkt.tls, "handshake_extensions_server_name", "Unknown")
            packet_data["tls_version"] = getattr(pkt.tls, "handshake_version", "Unknown")


        return [
            packet_data["protocol"],
            packet_data["host"],
            packet_data["url"],
            packet_data["method"],
            packet_data["content_type"],
            packet_data["sensitive_data"],
            packet_data["server_name"],
            packet_data["cipher_suite"],
            packet_data["issuer"],
            packet_data["subject"],
            packet_data["unstrusted_cert"],
            packet_data["tls_version"],
            packet_data["expire_certificate"],
            packet_data["hsts"]
        ]

    except Exception as e:
        logger.error(f"{str(e)}")
        return None

def main():
    try:
        logger.info(f"{PCAP_FILE}")


        cap = pyshark.FileCapture(PCAP_FILE, display_filter="http or tls")


        data = []
        for pkt in cap:
            packet_data = process_packet(pkt)
            if packet_data:
                data.append(packet_data)

        # Đóng file PCAP
        cap.close()

        # Tạo DataFrame
        df = pd.DataFrame(data, columns=[
            "protocol", "host", "url", "method", "content_type", "sensitive_data",
            "server_name", "cipher_suite", "issuer", "subject", "unstrusted_cert",
            "tls_version", "expire_certificate", "hsts"
        ])


        unique_servers = df[df['protocol'] == 'TLS']['server_name'].unique()
        server_info = {}



        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_server = {
                executor.submit(get_certificate_info, server): server
                for server in unique_servers if server != "Unknown"
            }

            for future in future_to_server:
                server = future_to_server[future]
                try:
                    server_info[server] = future.result()
                except Exception as e:
                    logger.error(f"Lỗi khi xử lý {server}: {str(e)}")


        for index, row in df[df['protocol'] == 'TLS'].iterrows():
            server = row['server_name']
            if server in server_info:
                info = server_info[server]
                df.at[index, 'cipher_suite'] = info['cipher_suite']
                df.at[index, 'unstrusted_cert'] = info['unstrusted_cert']
                df.at[index, 'expire_certificate'] = info['expire_certificate']


        df.to_csv(CSV_FILE, index=False)


    except Exception as e:
        logger.error(f"{str(e)}")

if __name__ == "__main__":
    main()
    #1: sercure, 0:insecure
    df = pd.read_csv(CSV_FILE)


    # 1: Secure, 0: Insecure
    # df['weak_cipher_suite'] = np.where(df['cipher_suite'] == 'Unknown', 0, 1)
    # df['certificate'] = np.where(df['unstrusted_cert'] == 'Yes', 0, 1)  # Fixed typo
    # df['expired_certificate'] = np.where(df['expire_certificate'] == 'Expired', 0, 1)
    # df['downgrade'] = np.where((df['protocol'] == 'HTTP') & (df['hsts'] == 'No'), 0, 1)
    # df['weak_tls_version'] = np.where((df['protocol'] == 'TLS') & ~df['tls_version'].isin(['0x0303', '0x0302', 'Unknown']), 0, 1)
    # df['sensitive_http'] = np.where((df['sensitive_data'].notna()) & (df['protocol'] == 'HTTP'), 0, 1)

    # df["secure"] = np.where(
    #     (df['weak_cipher_suite'] == 0) |
    #     (df['certificate'] == 0) |
    #     (df['expired_certificate'] == 0) |
    #     (df['downgrade'] == 0) |
    #     (df['sensitive_http'] == 0) |
    #     (df['weak_tls_version'] == 0),
    #     0,  # Insecure
    #     1   # Secure
    # )

    print(df['secure'].value_counts())
    df.to_csv(CSV_FILE)
