http://blog.csdn.net/bosong_123/article/details/52495750

MySQL 的大多数事务型存储引擎实现的都不是简单的行级锁，基于提高并发性的考虑，它们一般都同时实现了多个版本并发控制(MVCC）。不仅是MySQL，包括Orcale，PostgreSQL等其他数据库系统也都实现了MVCC，但是它们的实现机制不尽相同，因为MVCC没有一个统一的标准。

可以认为MVCC是行级锁的一个变种，但是它在很多情况下可以避免加锁操作，因此开销更低。虽然各个数据库管理系统实现MVCC的机制不尽相同，但大都实现了非阻塞的读操作，写操作也只是锁定必要的行。



在MySQL中，MVCC的实现是通过保存数据在某个时间点的快照来实现的。也就是说，不管需要执行多长时间，每个事务看到的数据都是一致的。根据事务开始时间的不同，每个事务对同一张表，同一时刻看到的数据可能不一样。



MVCC,一个行级锁的变种,很多情况下避免了加锁操作,开销更低.实现非阻塞的读操作,写操作也只锁定必要的行.