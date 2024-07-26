from collections import defaultdict as dd
from copy import deepcopy
import datetime

def convert():
    input_lines = open("polylogger_format_input.txt", 'r').readlines()
    chunk_size = 3
    assert len(input_lines)/chunk_size == len(input_lines)//chunk_size, f"Got {len(input_lines)}, but expected it to be divisible by 3."
    chunked_input_lines = []
    tmp_l = []
    for l in input_lines:
        tmp_l.append(l.strip())
        if len(tmp_l) == 3:
            chunked_input_lines.append(deepcopy(tmp_l))
            tmp_l = []
    print(f"chunked_input_lines: {chunked_input_lines}")

    # Polylogger Logs have: Description / Project / DurationDate 
    #   Where DurationDate looks like:   "142 minutes2024-07-21"
    # Toggl expects:        Duration / Start Time / Start Date / Description / Project
    date2data_dict = dd(list)
    for l in chunked_input_lines:
        descr                   = l[0]
        proj                    = l[1]
        duration, date          = l[2].split("minutes")
        date2data_dict[date].append( (descr, proj, duration) )

    date2data_wStartTime_dict = dd(list)
    print(f"Data found, by date:")
    for i, (date, data) in enumerate(date2data_dict.items()):
        start_time = 1 # First activity begins 1 second into the day
        print(f"\n# {i}: {date} ---> {data}. Contained # of data items: {len(data)}")
        for item in data:
            descr, proj, duration = item
            duration = 60 * int(duration.strip())
            date2data_wStartTime_dict[date].append( (
                            str(datetime.timedelta(seconds=duration)), str(datetime.timedelta(seconds=start_time)), date, descr, proj) )
            start_time += duration + 1 # Next activity begins 1 second after last activity ended

    with open("toggl_format_output.txt", 'w') as wf:
        print(f"Data found (and will be written to toggl_format.txt), with properly formatted, distinct start times:")
        for i, (date, data) in enumerate(date2data_wStartTime_dict.items()):
            print(f"On date {date}:")
            for i, item in enumerate(data):
                print(f"\t# {i}: {item}")
                wf.write(','.join(item) + '\n')

if __name__ == "__main__":
    convert() 
