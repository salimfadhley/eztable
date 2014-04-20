from toytable import Table
p = Table([('Owner Id', int), 'Pokemon', ('Level', int)])
p.extend([
    [1, 'Pikachu', 18],
])
print p
o = Table([('Owner Id', int), ('Name', str)])
o.append([1, 'Ash Ketchum'])
o.append([2, 'Brock'])
o.append([3, 'Misty'])
print o
j = p.left_join(
    keys=('Owner Id',),
    other = o
)
print j
