# 环境配置
需采用Python3.7环境，按照requirements.txt进行安装
```
pip install -r requirements.txt
```

此外，需要额外安装解码器。

Windows下需要安装K-lite.exe

ubuntu下需安装
```
sudo apt-get install libgl1-mesa-dev
sudo apt-get install gstreamer1.0-libav
sudo apt-get install gstreamer1.0-plugins-bad
sudo apt-get install gstreamer1.0-plugins-base
sudo apt-get install gstreamer1.0-plugins-ugly
sudo apt-get install gstreamer1.0-plugins-good
sudo apt-get install libxcb-xinerama0
```

若出现提示qt.qpa.plugin: Could not load the Qt platform plugin……
首先，设置环境变量

```
export QT_DEBUG_PLUGINS=1
```

获取无法加载的so文件，若为opencv目录下的so文件，将其删除即可解决冲突。

```
rm venv/lib/python3.7/site-packages/cv2/qt/plugins/platforms/libqxcb.so
```

# 运行方式
运行主窗口：
```
python main.py
```

运行编辑工具
```
python modifier_main.py
```

测试数据请打开data目录下 group1 或 group1_clean 文件夹