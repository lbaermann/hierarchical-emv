import sys
from datetime import datetime
from pathlib import Path

import numpy as np


def _read_timing_file(p):
    for line in p.read_text().splitlines():
        parts = line.split(':')
        assert len(parts) == 2
        parts = [float(x.strip()) for x in parts]
        yield tuple(parts)


def main():
    base_dir = Path(sys.argv[1])
    received_file = base_dir / 'time_received_update.log'
    processed_file = base_dir / 'time_snapshot_finished.log'

    received = list(_read_timing_file(received_file))
    processed = list(_read_timing_file(processed_file))

    assert [v for k, v in received] == sorted(v for k, v in received)
    assert [v for k, v in processed] == sorted(v for k, v in processed)

    cutoff1 = datetime(2025, 12, 9, 12).timestamp()
    cutoff2 = datetime(2025, 12, 12, 1).timestamp()

    delays = []
    times = []
    for ts, received_state in received:
        if ts < cutoff1 or ts > cutoff2:
            continue

        ts2 = ts
        for ts2, processed_state in processed:
            if processed_state >= received_state:
                break
        delays.append(ts2 - ts)
        times.append(ts)

    print('mean', np.mean(delays))
    print('std', np.std(delays))
    print('median', np.median(delays))
    print('min', np.min(delays))
    print('max', np.max(delays))
    print('10% quantile', np.quantile(delays, 0.1))

    #print(list(zip(delays, times)))


if __name__ == '__main__':
    main()
