mydict = {'ab': 8.0, 'sd': 1.2, 'ac': 1.2, 'ad': 2}
print(mydict)
for tuple in sorted(mydict.items(), key=lambda x: (-x[1], (x[0]))):
    print(tuple)

print(sorted(mydict.items(), key=lambda x: (-x[1], (x[0]))))

a = {'1': {'a': 2}, '2': {'a': 2}, '3': {'a': 2}, '4': {'a': 2}}
for i in a.values():
    i['a'] = 4
print(a)