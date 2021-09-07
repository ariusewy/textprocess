import re
import sys
import os,glob

file =  open("118.xdc","r+")
file2 = open("108.xdc","r+")
result1 = open('118table.txt','w+')
pin_name = []
pin = []
for line in file.readlines():
    a = line.split()
    if a !=[] and a[0]=='set_property'and a[1]=='PACKAGE_PIN':
        pin.append(a[2])
        pin_name.append(eval(a[4].strip( ']' )))
        print(a[2],a[4].strip( ']' ),file = result1)
    elif(a !=[] and a[0]=='#Other'and a[2]=='PACKAGE_PIN'):
        pin.append(a[3])
        pin_name.append(a[5].strip( ']' ))
        print(a[3],a[5].strip( ']' ),file = result1)

result1.close()

result2 = open('samename.txt','w+')
result3 = open('different.txt','w+')
same_vcu108_pin = []
same_vcu118_pin = []
for line in file2.readlines():
    b = line.split()
    if b !=[] and b[0]=='set_property' and b[1]=='PACKAGE_PIN':
        name = eval(b[4].strip( ']' ))
        if name in pin_name:
            index = pin_name.index(name)
            same_vcu108_pin.append(b[2])
            same_vcu118_pin.append(pin[index])
            print('vcu118_pin_name_id=',index,name,'vcu108_pin:',b[2],'vcu118_pin:',pin[index],file=result2)
        else:
            print('vcu108_pin_name',name,'vcu108_pin:',b[2],file=result3)
    elif b !=[] and b[0]=='#Other' and b[2]=='PACKAGE_PIN':
        name = b[5]
        if name in pin_name:
            index = pin_name.index(name)
            same_vcu108_pin.append(b[3])
            same_vcu118_pin.append(pin[index])
            print('vcu118_pin_name_id=',index,name,'vcu108_pin:',b[3],'vcu118_pin:',pin[index],file=result2)
        else:
            print('vcu108_pin_name',name,'vcu108_pin:',b[3],file=result3)
       
result2.close()
result3.close()

print(same_vcu118_pin[198])

file = open('vcu108shell.scala','r+')
unknow=[]
report_yes = open('report_yes','w+')
report_on = open('report_no','w+')
def search(temp):
    strNum = temp.group()
    for element in strNum.split():
        element = eval(element)
        if element in same_vcu118_pin:
            index = same_vcu118_pin.index(element)
            print('118_pin is',element,'has been CHANGED to 108_pin:',same_vcu108_pin[index])
            print('\t',element,same_vcu108_pin[index],file=report_yes)
            return str('"'+same_vcu108_pin[index]+'"')
        else:
            if element in pin:
                index = pin.index(element)
                print('manual change:',element,'pin_name is:',pin_name[index])
                print('\t',element,pin_name[index],file=report_on)
                return str('"TODO_'+element+'"')
            else:
                print('NOT FOUND:',element)
                print(element,file=report_on)
                return str('"TODO_'+element+'"')

newshell  = open('newshell.scala','w+')
for line in file.readlines():
    if line.strip().startswith('/*') or line.strip().startswith('//'):
        print(line,file=newshell)
    else:
        print(re.sub(r'"([A-Z][A-Z]?[0-9][0-9]?)"', search, line),file=newshell)

file.close()
report_on.close()
report_yes.close()


