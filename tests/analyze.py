
from valvepcf.unloader import *

# This is a bunch of functions to debug test errors.
# They help to find discrepancies between inputs and outputs


def pstr(strings, sid):
    if isinstance(sid, int):
        return strings[sid]
    else:
        return sid


def analyze_elements(pcf):
    original = pcf._data
    recreated = unload_pcf(pcf)
    passed = True
    if len(original.elements) != len(recreated['elements']):
        print('diff len')
        passed = False

    for i in range(len(original.elements)):
        orig = original.elements[i].elementName
        copy = recreated['elements'][i]['elementName']
        if isinstance(orig, int):
            orig = original.strings[orig]
        if isinstance(copy, int):
            copy = recreated['strings'][copy]

        if orig != copy:
            print(orig + ' = ' + copy)
            passed = False

    if not passed:
        print('diff elements ' + str(len(recreated['elements'])))

    return passed


def analyze_attributes(pcf):
    original = pcf._data
    recreated = unload_pcf(pcf)
    passed = True
    problems = []

    if len(original.attributes) != len(recreated['attributes']):
        print('diff attributes')
        passed = False

    for i in range(len(recreated['attributes'])):
        orig = original.attributes[i]
        copy = recreated['attributes'][i]

        if len(orig) != len(copy):
            passed = False
            print('attr len mismatch')
            print(str(len(orig)) + ' - ' + str(len(copy)))

        for j in range(len(orig)):
            o = orig[j].attributeData
            c = copy[j]['attributeData']
            to = orig[j].attributeType

            if isinstance(o, ListContainer):
                o = list(o)
            if to == 5 and isinstance(o, int):
                o = pstr(original.strings, o)
            if to == 5 and isinstance(c, int):
                c = pstr(recreated['strings'], c)

            if o != c:
                passed = False
                print(str(i) + '-' + str(j) + ' - ' + str(o) + '<->' + str(c))

    return passed


def analyze_strings(pcf):
    original = pcf._data
    recreated = unload_pcf(pcf)
    passed = True

    for s in original.strings:
        if s not in recreated['strings']:
            passed = False
            print('missing: ' + s)

    for s in recreated['strings']:
        if s not in original.strings:
            passed = False
            print('extra: ' + s)

    if not passed:
        return passed

    for i in range(len(recreated['strings'])):
        if original.strings[i] != recreated['strings'][i]:
            if i >= 1 and passed:
                print(str(i-1) + ' - ' + original.strings[i-1] +
                      ' <> ' + recreated['strings'][i-1])
            passed = False
            print(str(i) + ' - ' +
                  original.strings[i] + ' <> ' + recreated['strings'][i])
    return passed
