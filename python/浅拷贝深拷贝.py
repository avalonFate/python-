import copy
"""
copy.copy：浅拷贝，只拷贝父对象(容器)，不拷贝父对象的子(容器)对象。
copy.deepcopｙ：深拷贝，拷贝父对象和子(容器)对象。
"""
'''
在python中对于非容器类型没有拷贝这一说
Python容器类型 列表、元组、字典
'''
c = 'acc'
d = 'acc'
print(c is d,'c和d指向一个内存')
"""
Python中对象之间的赋值只是传递引用，如果要拷贝对象需要使用标准模板中的copy
浅拷贝是默认的拷贝类型，序列类型的可以通过三种方式实现浅拷贝：1、完全切片操作；2、利用工厂函数，比如list()等；
3、使用copy模块中的copy()函数。。
“对一个对象进行浅拷贝其实是新创建了一个类型跟原对象一样，其内容是原来对象元素的引用，
换句话说，这个拷贝的对象本身是新的，但是它的内容不是。

"""
a = [1,2,[3,4],5,]
b = list(a)
print(id(a))
print(id(b))
print([id(x) for x in a])
print([id(x) for x in b])
"""
浅拷贝的A,B内容器对象[3,4](6,7)id值是一样的
"""
a[2].append(3)
print(a)
print(b)
"""
a[2]变了
b也变了
"""
"""
可以看到b作为浅拷贝创立的新对象，与a的地址不同(id()结果可以认为是内存地址)，但是其内容数据的地址却是一致的.
"""
"""
copy.copy：浅拷贝，只拷贝父对象(容器)，不拷贝父对象的子(容器)对象。
copy.deepcopｙ：深拷贝，拷贝父对象和子(容器)对象。
浅拷贝只能做顶层复制，但是不能复制其嵌套的数据结构。
"""
a = [1,2,[3,['666'],4],5,]
b = copy.deepcopy(a)
print("深拷贝的a",[id(x) for x in a])
print("深拷贝的b",[id(x) for x in b])
a[2].append('9999')
print(a)
print(b)
'深拷贝后a的子对象变了,不影响b'
print(id(a[2][1]))
print(id(b[2][1]))
"""
深拷贝是对于一个对象所有层次的拷贝(递归)
"""