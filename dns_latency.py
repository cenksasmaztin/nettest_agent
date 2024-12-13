import dns.resolver
import time
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Teste dahil edilecek DNS adresleri
DNS_LIST = [
    "google.com", "facebook.com", "amazon.com", "yahoo.com", 
    "wikipedia.org", "twitter.com", "instagram.com", "linkedin.com", 
    "microsoft.com", "apple.com", "netflix.com", "reddit.com", 
    "yandex.ru", "baidu.com", "bing.com", "ebay.com", 
    "bbc.co.uk", "cnn.com", "espn.com", "spotify.com"
]

# Test sonuçlarını saklamak için listeler
test_results = []
timestamps = []

def perform_dns_test():
    latencies = []
    resolver = dns.resolver.Resolver()
    for dns_name in DNS_LIST:
        try:
            start_time = time.time()
            resolver.resolve(dns_name, 'A')  # A kaydı sorgusu
            latency = (time.time() - start_time) * 1000  # ms cinsinden
            latencies.append(latency)
        except Exception as e:
            latencies.append(None)  # Hatalı sorgu için None ekle
    return latencies

def generate_report(test_number, latencies):
    avg_latency = sum([lat for lat in latencies if lat is not None]) / len([lat for lat in latencies if lat is not None])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = f"dns_latency_reports/report_{test_number}.txt"
    os.makedirs("dns_latency_reports", exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write(f"DNS Latency Test Report #{test_number}\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        for dns_name, latency in zip(DNS_LIST, latencies):
            f.write(f"{dns_name}: {latency if latency is not None else 'Timeout'} ms\n")
        f.write(f"\nAverage Latency: {avg_latency:.2f} ms\n")
        f.write("\n---\nOxoo Network Agent DNS Latency Test\n")
    
    return avg_latency

def plot_results():
    os.makedirs("dns_latency_reports", exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, test_results, marker="o", linestyle="-")
    plt.xlabel("Timestamp")
    plt.ylabel("Average Latency (ms)")
    plt.title("DNS Latency Over Time")
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("dns_latency_reports/dns_latency_graph.png")
    plt.close()

def main():
    test_number = 1
    while True:
        print(f"Starting Test #{test_number}")
        latencies = perform_dns_test()
        avg_latency = generate_report(test_number, latencies)
        test_results.append(avg_latency)
        timestamps.append(datetime.now().strftime("%H:%M:%S"))
        plot_results()
        print(f"Test #{test_number} completed. Average Latency: {avg_latency:.2f} ms")
        test_number += 1
        time.sleep(180)  # 3 dakika bekle

if __name__ == "__main__":
    main()