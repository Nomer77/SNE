a = {1: 0, 2: 0, 3: 0}
for k, v in a.items():
    print(f"k = {k}, v = {v}")
    if v == 0:
        a[k] = None

print(a)