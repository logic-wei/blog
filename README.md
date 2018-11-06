# logic wei的博客

## 博客目录

- [按类别](./SUMMARY-CATEGORY.md)

- [按时间](./SUMMARY-DATE.md)

## 简介

基于markdown的博客框架。
此博客框架旨在：

- 避免复杂的html制作过程，专心于写作之上
- 能够方便的进行在线查阅
- 可以作为博客原始数据库，便于后续生成pdf、html等格式的文档用于其他用途
- 方便进行文件管理
- 不能因为框架的需要而对博客文件名或是博客内容进行过多无理的限制，影响写作的愉悦程度（说的就是jekyll）

怀着这样的想法，此博客框架被创造出来了，此框架既是一套规范，也是一套工具。

## gitblog.py

博客辅助工具，用于：

- 规范并自动生成目录结构
- 规范并自动生成文章内容
- 根据规范自动生成目录文件 

### 用法

```bash
# 新建Android分类
python3 tools/gitblog.py create -c Android
# Android分类下新建文章,名为helloworld
python3 tools/gitblog.py create -a helloworld -c Android
# 新建文章helloworld2,无分类
python3 tools/gitblog.py create -a helloworld2
# 在博客根目录生成博客目录文件
python3 tools/gitblog.py summary
```

## 概念

### 根目录结构

先看看根目录结构

```bash
.
├── articles # 文章根目录
│   └── example # 文章标题
│       ├── imgs # 文章图片资源
│       │   └── 20181023-142658.png
│       └── main.md # 文章内容
├── tools # 博客管理工具
│   └── gitblog.py
├── README.md # 博客主页
├── SUMMARY-CATEGORY.md # 按分类排列的博客目录
└── SUMMARY-DATE.md # 按时间排序的博客目录
```

### 文章（article）

`文章`定义为包含`main.md`的文件夹，为了保持`文章`的独立性，资源文件通通放入这个文件夹内，`文章`可以放在`articles`中，也可以放在`分类`下

```bash
[文章名]{
    imgs/
    main.md
}
```

### 分类(category)

`分类`定义为一个普通文件夹（不包含main.md的文件夹），`文章`可以放入到`分类`中，`分类`不可以嵌套，`分类`只能放在`articles`下

```bash
[分类名]{
    [文章名0]{
        imgs/
        main.md
    }
    [文章名1]{
        imgs/
        main.md
    }
}
```
