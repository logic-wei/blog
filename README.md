# logic wei的博客

基于github的博客。此仓库用作我博客的原始数据库，为了便于查阅和编辑，同时编写了相应的工具作为辅助

## 目录

- [分类列表](./SUMMARY-CATEGORY.md)
- [时间排序](./SUMMARY-DATE.md)


## gitblog.py

博客辅助工具，用于：

- 规范目录结构
- 根据目录结构自动生成目录文件 

### 用法

```bash
python tools/gitblog.py create -c Android # 新建Android分类
python tools/gitblog.py create -a helloworld -c Android # Android分类下新建文章,名为helloworld
python tools/gitblog.py create -a helloworld2 # 新建文章helloworld2,无分类
python tools/gitblog.py summary  # 在根目录生成博客目录文件
```

## 概念

### 根目录结构
先看看根目录
```bash
.
├── articles # 文章根目录
│   └── example # 文章标题
│       ├── imgs # 文章图片资源
│       │   ├── 20181023-142658.png
│       │   ├── 20181023-142953.png
│       │   ├── 20181023-142959.png
│       │   └── 20181023-143108.png
│       └── main.md # 文章内容
├── gitblog.py # 博客管理工具
├── README.md # 博客主页
└── SUMMARY.md # 博客目录
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
