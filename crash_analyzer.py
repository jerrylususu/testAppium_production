import json


def convert_json_to_log(json_log: str) -> str:
    log_array = json.loads(json_log)
    log = ''
    for log_entry in log_array:
        log += log_entry['message'] + '\n'
    return log


def extract_crash(log: str) -> str:
    crash_start = log.find('E AndroidRuntime: FATAL EXCEPTION:')
    crash_start = log.rfind('\n', 0, crash_start) + 1
    if crash_start == -1:
        return ''
    crash_end_start = crash_start
    crash_end = log.find('\n', crash_start) + 1
    while 'E AndroidRuntime:' in log[crash_end_start:crash_end]:
        crash_end_start = crash_end
        crash_end = log.find('\n', crash_end) + 1
    crash_end = crash_end_start
    return log[crash_start:crash_end]
