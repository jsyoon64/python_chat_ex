a = dict(one=1, two=2, three=3)
b = {'one':1, 'two':2, 'three':3, 'four':4}
print(a)
print(b)

if(len(b)>len(a)):
    res = b.keys() - a.keys()

print(res)

res_dict = {k:b[k] for k in res}
print(res_dict)