import statistics
import subprocess
from datetime import datetime

def ping_host(host, count=4):
    """Ping a host and return latency times in ms"""
    times = []
    try:
        output = subprocess.check_output(
            ["ping", "-c", str(count), host],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        # Extract time values from ping output (Linux/macOS format)
        for line in output.splitlines():
            if "time=" in line:
                time_ms = float(line.split("time=")[1].split(" ms")[0])
                times.append(time_ms)
    except subprocess.CalledProcessError:
        print(f"Could not ping {host}")
    return times

def analyze_latency(times):
    """Calculate latency statistics"""
    if not times:
        return None
    return {
        "avg": statistics.mean(times),
        "min": min(times),
        "max": max(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        "samples": len(times)
    }

def main():
    print("=== Network Latency Analyzer ===")
    host = input("Enter host (e.g., google.com or 8.8.8.8): ")
    count = int(input("Ping count (default 4): ") or 4)
    
    print(f"\nPinging {host} {count} times...")
    start = datetime.now()
    times = ping_host(host, count)
    latency = analyze_latency(times)
    
    if latency:
        print(f"\nResults for {host}:")
        print(f"Average: {latency['avg']:.2f} ms")
        print(f"Minimum: {latency['min']:.2f} ms")
        print(f"Maximum: {latency['max']:.2f} ms")
        print(f"Jitter: ±{latency['stdev']:.2f} ms (stdev)")
        print(f"Test duration: {(datetime.now() - start).total_seconds():.2f}s")
    else:
        print("No valid responses received.")

if __name__ == "__main__":
    main()