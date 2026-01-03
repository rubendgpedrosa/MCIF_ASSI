import hashlib
import time
import secrets
import sys
# Needed for the modern algorithms
import bcrypt
from argon2 import PasswordHasher, Type

# --- INITIAL SETUP ---
# Using a fixed string to keep tests fair
PASSWORD = b"IPLEIRIA"
# High iterations for fast hashing to average out CPU noise
ITERATIONS_FAST = 100000
# Low iterations for slow hashing because they are... slow
ITERATIONS_SLOW = 10
# !--- INITIAL SETUP ---!

class HashService:
    def run_md5(self, pwd):
        # Legacy/Broken
        return hashlib.md5(pwd).hexdigest()

    def run_sha1(self, pwd):
        # Legacy/Broken
        return hashlib.sha1(pwd).hexdigest()

    def run_sha256_unsalted(self, pwd):
        # Fast but can be risky without salt as we can use hash tables
        return hashlib.sha256(pwd).hexdigest()

    def run_sha256_salted(self, pwd):
        # Better, adds salt, prevents hash tables
        salt = secrets.token_bytes(16)
        return hashlib.sha256(salt + pwd).hexdigest()

    def run_bcrypt(self, pwd, cost=12):
        # Adaptive work factor
        salt = bcrypt.gensalt(rounds=cost)
        return bcrypt.hashpw(pwd, salt)

    def run_argon2(self, pwd):
        # Modern standard (OWASP params)
        ph = PasswordHasher(
            time_cost=2, 
            memory_cost=64000, # 64mb
            parallelism=2, 
            hash_len=32, 
            salt_len=16,
            type=Type.ID
        )
        # library expects string, not bytes
        return ph.hash(pwd.decode('utf-8'))

def benchmark(algoName, callback, iterations):
    print(f"[*] Benchmarking {algoName} ({iterations} runs)...")
    
    startTime = time.perf_counter()
    
    for i in range(iterations):
        callback(PASSWORD)
        
    endTime = time.perf_counter()
    totalTime = endTime - startTime
    
    avgTime = totalTime / iterations
    throughput = 1 / avgTime if avgTime > 0 else 0
    
    return {
        "name": algoName,
        "timeMs": avgTime * 1000,
        "throughput": throughput
    }

def print_manual_table(results):
    # Table headers
    headers = ["Algorithm", "Cost per Attempt", "Attacker Throughput (H/s)"]

    # Column widths
    w1, w2, w3 = 20, 20, 29

    # Draw separator line
    def draw_line(char="-", junction="+"):
        print(f"{junction}{char*(w1+2)}{junction}{char*(w2+2)}{junction}{char*(w3+2)}{junction}")

    # Draw Header
    draw_line("-", "+")
    print(f"| {headers[0]:<{w1}} | {headers[1]:<{w2}} | {headers[2]:<{w3}} |")
    draw_line("=", "+")

    # Draw Rows
    for row in results:
        costStr = f"{row['timeMs']:.4f} ms"
        throuputStr = f"{row['throughput']:.2f}"
        print(f"| {row['name']:<{w1}} | {costStr:<{w2}} | {throuputStr:<{w3}} |")
        draw_line("-", "+")

if __name__ == "__main__":
    # Check for password parameter
    if len(sys.argv) > 1:
        PASSWORD = sys.argv[1].encode('utf-8')
    
    service = HashService()
    results = []

    print("--- INIT PASSWORD CRACK ---")
    print(f"Target Password: {PASSWORD.decode()}")

    # Benchmarks
    # Fast Algorithms
    results.append(benchmark("MD5", service.run_md5, ITERATIONS_FAST))
    results.append(benchmark("SHA-1", service.run_sha1, ITERATIONS_FAST))
    results.append(benchmark("SHA-256 (Unsalted)", service.run_sha256_unsalted, ITERATIONS_FAST))
    results.append(benchmark("SHA-256 (Salted)", service.run_sha256_salted, ITERATIONS_FAST))

    # Slow Algorithms
    results.append(benchmark("Bcrypt (Cost=12)", lambda p: service.run_bcrypt(p, 12), ITERATIONS_SLOW))
    results.append(benchmark("Argon2id (OWASP)", service.run_argon2, ITERATIONS_SLOW))

    # Output
    print("\n" + "="*80)
    print("BENCHMARK RESULTS")
    print("="*80)

    print_manual_table(results)

    print("\n[!] INTERPRETATION:")
    print("    Higher Throughput = Lower Security (Easier to Brute Force)")
    print("    Higher Cost = Higher Security (Resistant to Brute Force)")