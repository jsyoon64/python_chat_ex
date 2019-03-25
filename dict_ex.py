def_control = {'PDxx':{'PA':0,'PB':0,'LED':0,'STYLE':0}}
id_lists = {}


pdgen = {}
#pdgen['PD01'] = def_control['PDxx']
#copy()를 써야 함.
pdgen['PD01'] = def_control['PDxx'].copy()
id_lists.update(pdgen)
print(id_lists)
id_lists['PD01']['PA'] = 1
print(id_lists)

pdgen['PD02'] = def_control['PDxx'].copy()
id_lists.update(pdgen)
print(id_lists.keys())
print(id_lists)

pdgen['PD02'] = def_control['PDxx'].copy()
pdgen['PD02']['PB'] = 1
id_lists.update(pdgen)
print(id_lists)
print(def_control)

print("PD01.PA=",id_lists['PD01']['PA'])

if "PD01" in id_lists:
    print("PD01이 dict에 있음")