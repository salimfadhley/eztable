from eztable import Table
o = Table([('Owner Id', int), ('Name', str)])
o.extend([[1, 'Ash Ketchum'],
          [2, 'Brock'],
          [3, 'Misty']])
print(o)
