## Mysql 索引概述

所有存储引擎支持每个表至少16 个索引，总索引长度至少为256 字节。大多数存储引擎有更高的限制。

在MySQL 5.1 中，对于MyISAM 和InnoDB 表，前缀可以达到1000 字节长。请注意前缀的限制应以字节为单位进行测量，而CREATE TABLE 语句中的前缀长度解释为字符数。当为使用多字节字符集的列指定前缀长度时一定要加以考虑。

还可以创建FULLTEXT 索引。该索引可以用于全文搜索。只有MyISAM 存储引擎支持FULLTEXT 索引，并且只为CHAR、VARCHAR 和TEXT 列。索引总是对整个列进行，不支持局部(前缀)索引.



MySQL数据库中，有四种索引：聚集索引(主键索引)、普通索引,唯一索引,全文索引.



### 电商项目中商品详情--使用了全文索引

#### 全文索引和普通索引的区别

普通索引的结构主要以B+树和哈希索引为主，用于实现对字段中数据的精确查找，比如查找某个字段值等于给定值的记录，A=10这种查询，因此适合数值型字段和短文本字段.

#### 大字段不适合做普通索引，是因为索引大型字段会让索引占用太多的存储空间。普通索引过长,很多引擎不支持.

全文索引(也称全文检索)是目前搜索引擎使用的一种关键技术。它能够利用「分词技术「等多种算法智能分析出文本文字中关键字词的频率及重要性.也可以按照词频和重要性进行排序.

* 普通索引则只支持like查询有没有,不支持按照词频进行排序.

在数据库中进行模糊查询是使用`LIKE`关键字进行查询，例如：

```mysql
# 普通索引的模糊查询
SELECT * FROM article WHERE content LIKE '%查询字符串%'
#like查询特别的慢
#全文索引的查询
SELECT * FROM article WHERE MATCH(title, content) AGAINST('查询字符串')
```

mysql中MyISAM支持全文索引.

InnoDB引擎对FULLTEXT索引的支持是MySQL5.6新引入的特性，之前只有MyISAM引擎支持FULLTEXT索引。对于FULLTEXT索引的内容可以使用MATCH()…AGAINST语法进行查询。



### 设计索引的原则

1.最适合索引的列是出现在WHERE 子句中的列，或连接子句中指定的列，而不是出现在SELECT 关键字后的选择列表中的列。

2.使用惟一索引。考虑某列中值的分布。对于惟一值的列，索引的效果最好，而具有多个重复值的列，其索引效果最差。例如，存放年龄的列具有不同值，很容易区分各行。而用来记录性别的列，只含有“ M”和“F”，则对此列进行索引没有多大用处（不管搜索哪个值，都会得出大约一半的行）.

3.使用短索引。如果对串列进行索引，应该指定一个前缀长度，只要有可能就应该这样做。例如，如果有一个CHAR(200) 列，如果在前10 个或20 个字符内，多数值是惟一的，那么就不要对整个列进行索引。对前10 个或20 个字符进行索引能够节省大量索引空间，也可能会使查询更快。较小的索引涉及的磁盘I/O 较少，较短的值比较起来更快。更为重要的是，对于较短的键值，索引高速缓存中的块能容纳更多的键值，因此，MySQL也可以在内存中容纳更多的值。这增加了找到行而不用读取索引中较多块的可能性。

4.利用最左前缀。在创建一个n 列的索引时，实际是创建了MySQL 可利用的n 个索引。多列索引可起几个索引的作用，因为可利用索引中最左边的列集来匹配行。这样的列集称为最左前缀。（这与索引一个列的前缀不同，索引一个列的前缀是利用该的前n 个字符作为索引值。）

5.不要过度索引。不要以为索引“越多越好”，什么东西都用索引是错的。每个额外的索引都要占用额外的磁盘空间，并降低写操作的性能，这一点我们前面已经介绍过。在修改表的内容时，索引必须进行更新，有时可能需要重构，因此，索引越多，所花的时间越长。

6.考虑在列上进行的比较类型。索引可用于“ <”、“ < = ”、“ = ”、“ > =”、“ >”和BETWEEN 运算。在模式具有一个直接量前缀时，索引也用于LIKE 运算。如果只将某个列用于其他类型的运算时（如STRCMP( )），对其进行索引没有价值。



### btree 索引与hash 索引

。优化器不能使用hash 索引来加速ORDER BY 操作。

B-tree 索引可以用于使用 =, >, >=, <, <= 或者 BETWEEN 运算符的列比较。如果 LIKE 的参数是一个没有以通配符起始的常量字符串的话也可以使用这种索引。如like Lisa%

有时，即使有索引可以使用，MySQL 也不使用任何索引。发生这种情况的场景之一就是优化器估算出使用该索引将要求 MySql 去访问这张表的绝大部分记录。这种情况下，一个表扫描可能更快

```mysql
下列范围查询适用于btree 索引和hash 索引
SELECT * FROM t1 WHERE key_col = 1 OR key_col IN (15,18,20);
下列范围查询适用于btree 索引
SELECT * FROM t1 WHERE key_col > 1 AND key_col < 10;
SELECT * FROM t1 WHERE key_col LIKE 'ab%' OR key_col BETWEEN 'bar' AND
'foo';
```



## Mysql 如何使用索引

索引用于快速找出在某个列中有一特定值的行。不使用索引，MySQL 必须从第1 条记
录开始然后读完整个表直到找出相关的行。表越大，花费的时间越多。如果表中查询的列有
一个索引，MySQL 能快速到达一个位置去搜寻到数据文件的中间，没有必要看所有数据。如
果一个表有1000 行，这比顺序读取至少快100 倍。注意如果你需要访问大部分行，顺序读
取要快得多，因为此时我们避免磁盘搜索。(找到索引,再通过索引去找数据,读两次磁盘)

大多数MySQL 索引(PRIMARY KEY、UNIQUE、INDEX 和FULLTEXT)在B 树中存储。只是
空间列类型的索引使用R-树，并且MEMORY 表还支持hash 索引。

