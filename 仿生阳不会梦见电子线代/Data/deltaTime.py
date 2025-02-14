def format_time(seconds):
    seconds = int(seconds)
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{days}天{hours}小时{minutes}分{seconds}秒"