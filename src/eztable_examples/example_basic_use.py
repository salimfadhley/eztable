from eztable import Table
p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
p.extend([
    [1, 'Pikachu', 18],
    [1, 'Bulbasaur', 22],
    [1, 'Charmander', 12],
    [3, 'Togepi', 5],
    [1, 'Starmie', 44],
    [9, 'Mew', 99],
])
print(p)
o = Table([('Owner Id', int), ('Name', str)])
o.append([1, 'Ash Ketchum'])
o.append([2, 'Brock'])
o.append([3, 'Misty'])
print(o)
j = p.left_join(
    keys=('Owner Id',),
    other=o
)
print(j)
j2 = j.project('Pokemon', 'Level', 'Name')
print(j2)
restricted = j2.restrict(['Name'], lambda n: n == 'Ash Ketchum')
print(restricted)
sliced = j2[1:4]
print(sliced)

j3 = j2.copy()
i = j3.add_index(('Pokemon',)).reindex()
print(i[('Pikachu',)])

# Have a nice day!
exit
exit