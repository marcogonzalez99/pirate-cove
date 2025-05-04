# perf.py
import time

DEBUG_PERF = False  # 🔁 Toggle ON/OFF here

class PerfMonitor:
    def __init__(self):
        self.enabled = DEBUG_PERF
        if self.enabled:
            self.sections = []
            self.start_time = time.time()

    def mark(self, label):
        if self.enabled:
            now = time.time()
            elapsed = (now - self.start_time) * 1000  # ms
            self.sections.append((label, elapsed))
            self.start_time = now

    def report(self):
        if not self.enabled:
            return
        total = sum([s[1] for s in self.sections])
        print("\n[PERF]")
        for label, elapsed in self.sections:
            print(f"  {label:<20}: {elapsed:.1f}ms")
        print(f"  {'TOTAL':<20}: {total:.1f}ms\n")
