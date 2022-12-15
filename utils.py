# Modulos utiles

e12series = ['10','12','15','18','22','27','33','39','47','56','68','82',]

# 5% tol (normally also available in 2% tolerance)
e24series = ['10','11','12','13','15','16','18','20','22','24','27','30',
    '33','36','39','43','47','51','56','62','68','75','82','91',]

# 2%
e48series = ['100','105','110','115','121','127','133','140','147','154',
    '162','169','178','187','196','205','215','226','237','249','261','274',
    '287','301','316','332','348','365','383','402','422','442','464','487',
    '511','536','562','590','619','649','681','715','750','787','825','866','909','953',]

# 1%
e96series = ['100','102','105','107','110','113','115','118','121','124','127',
    '130','133','137','140','143','147','150','154','158','162','165','169','174',
    '178','182','187','191','196','200','205','210','216','221','226','232','237',
    '243','249','255','261','267','274','280','287','294','301','309','316','324',
    '332','340','348','357','365','374','383','392','402','412','422','432','442',
    '453','464','475','487','499','511','523','536','549','562','576','590','604',
    '619','634','649','665','681','698','715','732','750','768','787','806','825',
    '845','866','887','909','931','953','976',]

def roundWithMultiplier(value):
    highMults = ['p','n','u','m','','K','M','G']
    offset = 4
    multCount = 0
    ogVal = value
    if(value >= 0.99):
        while (value // 999 > 0):
            value = value / 1000.0
            multCount += 1
    elif(value < 0.099):
        while (value < 0.099):
            value = value * 1000.0
            multCount -= 1

    if multCount < (-12) or multCount > 3:
        print("OUT OF RANGE:", multCount)
        multCount = 0
        
    ogVal = str(round(ogVal,3)).rstrip('0').rstrip('.')
    return [str(round(value,3)).rstrip('0').rstrip('.') + highMults[offset + multCount], ogVal]


def roundToRKM(value):
    highMults = ['R','K','M']
    multCount = 0
    value = float(value)
    ogVal = value
    if(value >= 0.99):
        while (value // 999 > 0):
            value = value / 1000.0
            multCount += 1
    # elif(value < 0.099):
    #     while (value < 0.099):
    #         value = value * 1000.0
    #         multCount -= 1

    if multCount > 3:
        print("OUT OF RANGE:", multCount)
        multCount = 0
        
    return [str(round(value,3)).rstrip('0').replace('.', highMults[multCount]), None]


def roundToPNU(value):
    highMults = ['p','n','u','m','']
    multCount = len(highMults) - 1
    value = float(value)
    # if(value >= 0.99):
    #     while (value // 999 > 0):
    #         value = value / 1000.0
    #         multCount += 1
    if(value < 0.099):
        while (value < 0.099):
            value = value * 1000.0
            multCount -= 1

    if multCount < 0:
        print("OUT OF RANGE:", multCount)
        multCount = 0
        
    return [str(round(value,3)).strip('0').replace('.', highMults[multCount]), None]

# testList = [0.47, 1.13, 100, 1000, 4700, 5360, 1270000]

# for val in testList:
#     val = val * 10**(-12)
#     print(roundToPNU(val), val)


def xxyMarkingValue(e12str, power):
    value = (float(e12str) * (10** power)) * 10.0**(-12) # pico
    mark = [roundWithMultiplier(value)[0]]
    return mark

def xxMarkingValue(e12str):
    value = float(e12str) * 10.0**(-9) # nano
    mark = [roundWithMultiplier(value)[0]]
    return mark

def x_xMarkingValue(e12str):
    value = float(e12str) * 10.0**(-10) # nano
    mark = [roundWithMultiplier(value)[0]]
    return mark


# for e12 in e12series:
#     print(x_xMarkingValue(e12))
