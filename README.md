### 概述

企业机务管理系统模板实现。

### 需要定制额外的内容

+ templates/security/login_user.html

每个用户的标题应该不同；且根据年份的不同，下面的版权时间也应该发生变化，必要情况下，可以根据不同的用户变更不同的图片信息。

+ modules/roles.py

不同公司显然具有不同的用户权限或名称，需要根据需要创建分支并进行更改

### 运维需要注意的内容

请查看企业内部文档有关**定制机务系统**的相关环境变量设置。尤其是对于MySQL数据库的设置，需要根据对应数据库访问连接中的数据库实例名，先进行必要的初始化，然后执行下述命令：

```
$ THY_SETTINGS=prod python manager.py reset_database --username 管理员的名称（默认为admin) --email 管理员的邮件地址（默认为admin@hfga.com.cn) --password 管理员的口令（默认为hfgahfga%）
```
