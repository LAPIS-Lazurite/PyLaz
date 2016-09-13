from PyLaz.PyLaz import *

lazurite = PyLaz()

result = lazurite.open()
print(result)

result = lazurite.begin(36,0xabcd,100,20)
print(result)

result = lazurite.send(0xffff,0xffff,"hello")
print(result)

result = lazurite.close()
print(result)

result = lazurite.remove()
print(result)


