class Category:
  def __init__(self, name):
    self.name = name
    self.ledger = []

  def deposit(self, amount, description = ''):
    self.ledger.append({'amount': amount, 'description': description})

  def withdraw(self, amount, description = ''):
    if self.check_funds(amount):
      self.ledger.append({'amount': -amount, 'description': description})
      return True
    else:
      return False

  def get_balance(self):
    return sum([item['amount'] for item in self.ledger])

  def transfer(self, amount, target):
    if self.check_funds(amount):
      self.withdraw(amount, 'Transfer to ' + target.name)
      target.deposit(amount, 'Transfer from ' + self.name)
      return True
    else:
      return False
  
  def check_funds(self, amount):
    return self.get_balance() >= amount
  
  def __str__(self):
    string = self.name.center(30, '*') + '\n'
    for item in self.ledger:
      description = (item['description'][:23] or item['description']).ljust(23)
      amount = ('{:.2f}'.format(item['amount'])[:7] or '{:.2f}'.format(item['amount'])).rjust(7)
      string += description + amount + '\n'
    string += 'Total: ' + str(self.get_balance())
    return string


def create_spend_chart(categories):
  total_spent = 0

  for i, item in enumerate(categories):
    category_total = 0

    for obj in item.ledger:
      category_total += obj['amount'] if obj['amount'] < 0 else 0

    total_spent += category_total
    categories[i] = tuple((item.name, category_total, item))

  total_spent = total_spent // 1
  categories = [(name, round(total / total_spent * 100), item) for name, total, item in categories]

  chart = ['Percentage spent by category']

  builder = 100
  while builder >= 0:
    string = str(builder).rjust(3) + '|'
    for category in categories:
      if category[1] >= builder:
        string += ' o '
      else:
        string += '   '
    chart.append(string + ' ')
    builder -= 10
  chart.append('    ' + ('---' * len(categories)) + '-')

  builder = sorted([len(category[0]) for category in categories])[-1]

  for i in range(builder):
    string = '    '
    for category in categories:
      if i < len(category[0]):
        string += f' {str(category[0])[i]} '
      else:
        string += '   '
    chart.append(string + ' ')
  
  return '\n'.join(chart)
