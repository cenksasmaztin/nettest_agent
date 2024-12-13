import requests
import time
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Test edilecek HTTPS adresleri
HTTPS_LIST = [
    "https://www.google.com", "https://www.facebook.com", "https://www.amazon.com", 
    "https://www.yahoo.com", "https://www.wikipedia.org", "https://www.twitter.com", 
    "https://www.instagram.com", "https://www.linkedin.com", "https://www.microsoft.com", 
    "https://www.apple.com", "https://www.netflix.com", "https://www.reddit.com",
    "https://www.yandex.ru", "https://www.baidu.com", "https://www.bing.com", 
    "https://www.ebay.com", "https://www.bbc.co.uk", "https://www.cnn.com", 
    "https://www.espn.com", "https://www.spotify.com"
]

# Test sonuçlarını saklamak için listeler
test_results = []
timestamps = []

def perform_https_test():
    latencies = []
    for url in HTTPS_LIST:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)  # 10 saniyelik timeout ile GET isteği
            if response.status_code == 200:
                latency = (time.time() - start_time) * 1000  # ms cinsinden
                latencies.append(latency)
            else:
                latencies.append(None)  # Hatalı yanıt
        except requests.exceptions.RequestException:
            latencies.append(None)  # Hata durumunda None ekle
    return latencies

def generate_report(test_number, latencies):
    avg_latency = sum([lat for lat in latencies if lat is not None]) / len([lat for lat in latencies if lat is not None])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = f"https_latency_reports/report_{test_number}.txt"
    os.makedirs("https_latency_reports", exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write(f"HTTPS Latency Test Report #{test_number}\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        for url, latency in zip(HTTPS_LIST, latencies):
            f.write(f"{url}: {latency if latency is not None else 'Timeout'} ms\n")
        f.write(f"\nAverage Latency: {avg_latency:.2f} ms\n")
        f.write("\n---\nOxoo Network Agent HTTPS Latency Test\n")
    
    return avg_latency

def plot_results():
    os.makedirs("https_latency_reports", exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, test_results, marker="o", linestyle="-")
    plt.xlabel("Timestamp")
    plt.ylabel("Average Latency (ms)")
    plt.title("HTTPS Latency Over Time")
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("https_latency_reports/https_latency_graph.png")
    plt.close()

def main():
    test_number = 1
    while True:
        print(f"Starting Test #{test_number}")
        latencies = perform_https_test()
        avg_latency = generate_report(test_number, latencies)
        test_results.append(avg_latency)
        timestamps.append(datetime.now().strftime("%H:%M:%S"))
        plot_results()
        print(f"Test #{test_number} completed. Average Latency: {avg_latency:.2f} ms")
        test_number += 1
        time.sleep(180)  # 3 dakika bekle

if __name__ == "__main__":
    main()