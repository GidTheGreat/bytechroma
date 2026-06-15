"""Cheap ansi rendering for ms websocket feed"""
import sys
import time
import threading


__version__ = "0.1.0"
class ByteChroma:
    def __init__(self, flush_interval=0.0):
        self.ESC = "\033"

        self.data = {}          # key -> value
        self.rows = {}          # key -> row
        self.next_row = 1

        self.dirty = set()

        self.flush_interval = flush_interval
        self._last_flush = 0

        self._lock = threading.Lock()

    # ---------- CORE UPDATE ----------
    def update(self, key, value):
        with self._lock:
            if key not in self.data:
                self.data[key] = value
                self.rows[key] = self.next_row
                self.next_row += 2
            else:
                if self.data[key] == value:
                    return
                self.data[key] = value

            self.dirty.add(key)

        if self.flush_interval == 0:
            self.flush()

    # ---------- MUTING ----------
    def mute(self, *keys):
        with self._lock:
            for k in keys:
                self.dirty.add(k)

    # ---------- RENDER SINGLE KEY ----------
    def _render(self, key):
        row = self.rows[key]

        # muted → clear only
        if key not in self.data or key is None:
            return ""

        if getattr(self, "_muted_set", None) and key in self._muted_set:
            return (
                f"{self.ESC}[{row};1H{self.ESC}[2K"
                f"{self.ESC}[{row+1};1H{self.ESC}[2K"
            )

        val = self.data[key]
        return (
            f"{self.ESC}[{row};1H"
            f"========{key}==========\n"
            f"{val:>15}"
        )

    # ---------- FLUSH ----------
    def flush(self):
        with self._lock:
            if not self.dirty:
                return

            out = []
            for k in self.dirty:
                out.append(self._render(k))

            sys.stdout.write("".join(out))
            sys.stdout.flush()

            self.dirty.clear()
            self._last_flush = time.time()

    # ---------- AUTO BUFFER MODE ----------
    def auto_flush_loop(self):
        """Call in a background thread if using flush_interval > 0."""
        print('start render')
        while True:
            time.sleep(self.flush_interval)
            self.flush()

if __name__ == "__main__":
    bc = ByteChroma()
    threading.Thread(target=bc.auto_flush_loop).start()
    bc.update("hey","you")
    bc.update("test","testing")
    bc.update("so far","so good")
    bc.mute("hey")
    print("after")