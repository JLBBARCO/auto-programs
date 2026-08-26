import datetime
import threading


_log_file = open("log.log", 'a+', encoding='utf-8')
_lock = threading.Lock()

# Only these levels are persisted to historic.json, matching the same
# typing already used in log.log (INFO, WARNING, ERROR). DEBUG messages
# stay in log.log only.
_HISTORIC_LEVELS = {'INFO', 'WARNING', 'ERROR'}


def _now():
    return datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')


def log(message, level="INFO"):
    now = _now()
    level = str(level).strip().upper()

    with _lock:
        _log_file.write(f'[{now}] [{level}] {message}\n')
        _log_file.flush()


def info(message):
    log(message, 'INFO')


def debug(message):
    log(message, 'DEBUG')


def warning(message):
    log(message, 'WARNING')


def error(message):
    log(message, 'ERROR')


# initial separator for new run
with _lock:
    _log_file.write('\n')
    _log_file.flush()
