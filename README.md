# sosblog
这是sosblog。  
GeoWat决定打造成一个共同开发，共同维护，提供内容的专栏博客。  
GeoWat想让这个项目开源、轻量、有趣。希望你也可以利用它一键部署自己的寝室博客。  
CSUJZZZ说hhvygutyrty

前端：
React + Ant Design：iamGeoWat  
后端：
Flask：Dormitabnia  
临时前端：  
VueJS + ElementUI

后端开发：  
1. 有更新后使用```pipenv sync```进行包依赖的同步
2. 在common.config.development中配置数据库信息
3. 打开python shell使用以下命令初始化数据库
```
from blog_backend.author import create_app, db
with create_app().test_request_context():
    db.create_all()
```