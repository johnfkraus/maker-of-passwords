intervals = (
    ('years', 31536000),  # 365 * 60 * 60 * 24 * 7
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

years5_4 =   5987369392383789062
print(display_time(49999999999444499, granularity=2))
print(display_time(499999, granularity=2))
print(display_time(years5_4, granularity=2))

