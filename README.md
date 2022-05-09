# screenshot
一个小玩意，一个截图和录屏的小工具

截图后，可以按任意键退出当前截屏状态

在Mac上报这个错： AttributeError: dlsym(0x7ff8574b4550, PyObjCObject_New): symbol not found 解决如下
```
pip install pyobjc-framework-Quartz==7.3
pip install pyobjc-framework-Cocoa==7.3
pip install pyobjc-framework-ApplicationServices==7.3
pip install pyobjc-core==7.3
```

代码在master分支里
