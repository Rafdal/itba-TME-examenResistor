# Modulos utiles

e12series = ['10','12','15','18','22','27','33','39','47','56','68','82',]


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


for e12 in e12series:
    print(x_xMarkingValue(e12))
