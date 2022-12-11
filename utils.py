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