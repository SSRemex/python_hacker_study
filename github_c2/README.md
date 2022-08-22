# github C&C
通过github仓库，进行控制
连接github仓库，远程加载仓库中的py文件，执行代码，返回结果提交至仓库中

`pip install github3.py`

## dirlister.py
列出当前目录

## enviroment.py
获取所有环境变量

## git_trojan.py
木马程序

**记录**
`sys.meta_path.append(GitImporter())`

`sys.meta_path` 为元加载器列表

`GitImporter` 为自定义加载器，用来远程github加载，也被称为`import hook`

