def printt(f):
  def inner(a, b):
    print(123)
    return f(a, b)
  return inner

@printt()
def sum_(a, b):
  return a + b

# print(type(sum_))
# printt(sum_)
