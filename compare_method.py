import json
import csv

with open("data/method.json") as r:
    method_data = json.load(r)

method_conclusion = method_data['conclusion']
method_verbose = method_data['verbose']

method_header = []
method_data = []

for _ in method_conclusion:
    method_header.append(_)
    method_data.append(method_conclusion[_])

with open("method_stat.csv", "a+", newline="") as w:
    writer = csv.writer(w)
    writer.writerow(method_header)
    writer.writerow(method_data)
    writer.writerow([])

verbose_identical = method_verbose['identical']
verbose_similar = method_verbose['similar']
verbose_new = method_verbose['new']
verbose_deleted = method_verbose['deleted']

verbose_header = ["method_signature", "lite", "full", "is_similar"]
verbose_data = []

for _ in verbose_identical:
    verbose_data.append([_, 1, 1, 0])

for _ in verbose_similar:
    verbose_data.append([_, 1, 1, 1])

for _ in verbose_new:
    verbose_data.append([_, 1, 0, 0])

for _ in verbose_deleted:
    verbose_data.append([_, 0, 1, 0])

with open("method_stat.csv", "a+", newline="") as w:
    writer = csv.writer(w)
    writer.writerow(verbose_header)
    for _ in verbose_data:
        writer.writerow(_)
