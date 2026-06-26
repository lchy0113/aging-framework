from pathlib import Path
from datetime import datetime


def make_log_path(category, prefix, index):
    log_dir = Path("logs") / category
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return log_dir / f"{prefix}_{index:04d}_{timestamp}.log"
