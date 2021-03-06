
# 从德化网采集房产信息,存入数据库进行房价分析

> 2018.3.12

> 2018.3.12

> 1.完成msql docker 安装

> 2.创建用户表user

> 3.创建操作数据库类

> 2018.3.13

> 1.创建房产表 room

> 2.插入用户数据和房产数据

> 2018.3.23 

> 发布1.0版本,实现卖房和租房模块开发

> 2018.4.2 

> 完成docker-compse测试

#开发环境:

```
iMAC  macOS High Sierra 10.13.2
python 3.6   
mysql 5.7.21
Sequel pro: 数据操作软件
```


# cmd 提交代码到git

```
git add *
git commit -m "出租房屋采集"
git push origin master
```


## python 生成项目依赖文件

```cmd
(venv)$ pip freeze >requirement.txt
```
安装依赖文件

```cmd
(venv)$ pip install -r requirement.txt
```

# 数据结构定义


使用Docker安装mysql搭建数据库开发环境

> 容器相关操作可以参考该文章<Docker — 从入门到实践> https://www.gitbook.com/book/yeasy/docker_practice

Mysql Docker 操作指南

> https://hub.docker.com/_/mysql
 

数据库存放本地目录

> /Users/fred/PycharmProjects/docker_v/mysql/data

```cmd
拉取mysql

docker pull mysql:5.7.21

docker run --name fred-mysql -p 3306:3306 -v /Users/fredliu/Documents/PycharmProjects/docker_v/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=fred123456 -d mysql:5.7.21

-p 3306:3306：将容器的3306端口映射到主机的3306端口


查看容器启动情况

docker ps 

```




docker容器常用操作


启动配置的容器
```html
docker start fred-mysql
docker start mynginx
```

列出镜像
docker images

删除悬空none镜像

docker rmi $(docker images -f "dangling=true" -q)

删除容器

docker rm container_id

删除镜像

docker image rm image_id
 

2.启动终止状态的容器
```cmd
docker container start fred-mysql
```

3.将一个运行态的容器终止，然后再重新启动它

```cmd
docker container restart  fred-mysql 

```



使用mysql存储数据

> 数据库名称 house

## BANNER 标题栏滚动图片

```
#20180330 暂时未启用
    id  int
    name VARCHAR(256) 标题栏图片名称
    title VARCHAR(256) 标题栏图片标题
    description VARCHAR(10240) 内容描述
    post_time datetime 发布时间
    start_time  datetime  --开始展示时间
    end_time    datetime  --结束展示时间

```

## USER 发布用户信息

```py
    # 字段信息
    # 用户信息   
    id          int          # 自增加值 
    name        VARCHAR(64)  # 发布人信息
    phone       VARCHAR(16)  # 联系方式 primary key 唯一值
    password    VARCHAR(256) # 用户登录密码
    type        VARCHAR(10)  # 用户特征 0:个人 1:经纪人
    #
    avatar     VARCHAR(64)  # 用户头像信息 上传到qiniu,md5值
    verify      int  # 用户是否认证 0 未认证, 1 认证
    # 公司信息
    company_name  VARCHAR(256)  # 公司名称
    company_addr  VARCHAR(512) # 公司地址


 
    
```

## Image 房屋图片信息

```sql

id int --自增id
room_sha_identity varchar(32) -- 房屋sha_identity外键
name      varchar(32)  --图片名称 
post_time datatime --上传照片时间
path      varchar(512) --图片存放地址
url       varchar(512) --图片存放地址
```

## Room 房屋信息

```sql
   -- 发布信息
    id           int --自增id
    sha_identity varchar(32) --md5(title+phone) 判断用户是否重复发布同一内容的房产信息
    phone        varchar(20) -- 用户联系方式,关联用户 外键
    title        varchar(256) -- 标题
    #
    
    # 房间类型
    post_time   datetime  -- 发布时间
    start_time  datetime  --开始时间
    end_time    datetime  --结束时间
    #
    
    
    # 房屋信息
    house_name  varchar(256) # 楼盘名称
    config      varchar(256) #房屋配置
    position    varchar(36) #房屋地址位置
    
    # 房屋信息
    price       float  # 价格
    pre_price   float #房屋单价
    area        float  # 面积
    floor       int  # 楼层
    total_floor int  # 总层高
    
    lobby       varchar(36)--客厅
    live_room   varchar(36)--卧室
    orientation varchar(36)--朝向
    type   varchar(36) --住宅/商铺
    has_kitchen_bath bool  # 是否有厨卫
    has_property_five bool  # 产权是否满五年
    mark        varchar(10240) #其他描述信息
    # 房屋图片介绍
    images = []

```

## Rent_Room 出租屋信息
```
   id           int --自增id
    sha_identity varchar(32) --md5(title+phone) 判断用户是否重复发布同一内容的房产信息
    phone        varchar(20) -- 用户联系方式,关联用户 外键
    title        varchar(256) -- 标题
    url         varchar(256) --采集的地址
    #

    # 房间类型
    post_time   datetime  -- 发布时间
    start_time  datetime  --开始时间
    end_time    datetime  --结束时间
    #


    # 房屋信息
    house_name  varchar(256) # 楼盘名称
    config      varchar(256) #房屋配置
    position    varchar(36) #房屋地址位置

    # 房屋信息
    price       float  # 价格
    area        float  # 面积
    floor       varchar(36)  # 楼层
    total_floor int  # 总层高
    rent_type   varchar(256) #出租类型

    lobby       varchar(36)--客厅
    live_room   varchar(36)--卧室
    orientation varchar(36)--朝向
    type   varchar(36) --住宅/商铺
    has_kitchen_bath bool  # 是否有厨卫
    mark        varchar(10240) #其他描述信息
    # 房屋图片介绍
    images = []
```


# 实现步骤:

1.采集数据

2.录入数据库

3.数据展示

4.用户注册发布数据

5.用户认领,绑定采集的手机号码




# 怎么搭建微信小程序的本地测试服务器

##问题的提出

Mac环境

> 方便快捷地搭建小程序的测试服务器

> 小程序对于网络请求的URL的特殊要求

> 不能出现端口号

> 不能用localhost

> 必须用https


安装nginx

```
docker run -d --name weixin-nginx -v /Users/fred/PycharmProjects/docker_v/nginx/conf/nginx.conf:/etc/nginx/nginx.conf:ro nginx

```

Git pull 强制覆盖本地文件

```
git fetch --all
git reset --hard origin/master
git pull
```