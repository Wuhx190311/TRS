# TRS
旅游管理系统（命令行版）

## 1、系统设计

**本程序采用层级结构，共分为：**

**1.**   **用户交互层**

​	**提供命令行交互接口**

**2.**   **流程控制层**

​	**封装了交互层可以使用的接口的具体实现**

**3.**   **用户层**

**	定义了三种用户：admin,customer,visitor**

**并定义每个用户可进行的操作**

**4.**   **资源管理层**

​	**封装了用户层每种用户方法的具体实现**

**5.**   **数据库接口层**

​	**提供了程序操作数据库的方式，并为resource_manager层提供基本的数据和数据库事务操作**

**每层为上层提供数据接口服务**

 

## 2、详细设计

### 	1. 数据库接口层

​	![image-20211216004237676](C:\Users\Whongxuan\AppData\Roaming\Typora\typora-user-images\image-20211216004237676.png)

### 	2.资源管理层 

<img src="C:\Users\Whongxuan\AppData\Roaming\Typora\typora-user-images\image-20211216004341998.png" alt="image-20211216004341998" style="zoom:50%;" />

### 	3.用户层

​	![image-20211216004438043](C:\Users\Whongxuan\AppData\Roaming\Typora\typora-user-images\image-20211216004438043.png)

### 	4.流程控制层

​		<img src="C:\Users\Whongxuan\AppData\Roaming\Typora\typora-user-images\image-20211216004513070.png" alt="image-20211216004513070" style="zoom:50%;" />  	

## 3.功能展示

![image-20211216005029604](C:\Users\Whongxuan\AppData\Roaming\Typora\typora-user-images\image-20211216005029604.png)
