# MOT展示界面功能接口
## tracking box 与 ws 数据接口
模块名称：operators.video_operator
### 方法
#### get_video_data(video_path: str, fps: float, use_clean_data) -> VideoDataCollection
获取对应视频文件的tracking_box数据和ws标注数据。
##### 参数
|参数名|类型|作用|
---|---|---
video_path|str|目标视频的路径，可用相对路径
fps|float|目标视频的帧率
use_clean_data|bool|是否使用clean标注。若为真，则读取data目录下clean.wsm文件，否则读取与视频同名的ws文件
##### 返回值
包含当前视频tracking_box数据和ws数据的VideoDataCollection

### 类
#### VideoDataCollection类
VideoDataCollection类为ws标注数据读取后的储存类。
#### \_\_init\_\_(self, data_path: str, ws_path: str, fps: float)
##### 参数
|参数名|类型|作用|
---|---|---
data_path|str|目标data文件路径（即tracking_box标注数据)
ws_path|str|目标ws文件路径
fps|float|目标视频的fps
#### 属性
以下属性均会在init方法中自动生成（通过文件IO方式）
##### data_list
为存放VideoData类的列表，是存储TrackingBox信息的核心属性。
```
data_list = [VideoData(240, 2, (240, 30, 60, 30)),...]
```

VideoData具有以下属性：

|属性|类型|作用|
---|---|---
frame|int|本条数据对应视频的帧数
no|int|Tracking Box的ID
vertexes|tuple|Tracking Box的坐标

例如需要在视频的第240帧，显示ID为2，坐标为（240，30，60，30）的box，则
```
frame = 240
no = 2
vertexes = (240, 30, 60, 30)
```

每个VideoData对象仅能存放一个时长为1帧的Tracking Box信息

##### ws_list
为存放ws信息的列表，是存储ws信息的核心属性

ws_list 的结构比较复杂。它是由以下信息构成的列表：
```
[(被跟踪id, 跟踪者id, 概率), ...]
```
ws_list所包含的信息在视频整个播放过程中均保持有效。

例如2号被3号跟踪，概率为0.3、5号被6号跟踪，概率为0.8，则ws_list的内容如下
```
[(2, 3, 0.3), (5, 6, 0.8)]
```
## 比较视图
### 比较逻辑
对比视图需要打开两个文件夹：主文件夹和比较文件夹。

主文件夹通过标题栏的"文件" -> "打开..." 进行选择，MOT会根据主文件夹下info.json载入视频列表，并记录所有的尾随文件。

对比文件夹通过标题栏的"文件" -> "打开比较目录..." 进行选择。在切换

### 文件要求
主文件夹必须有设置正确的info.json与对应的视频文件。每个视频文件需有同名的data文件。

对比文件夹中无需视频文件或info.json，但其下必须有与主文件夹同名的data文件。

例如以下的文件结构：

```
main_data\info.json
main_data\videos\1.avi
main_data\videos\1.data

compare_data\videos\1.data
```
在设置两个文件夹后，MOT将正确的对比两个"1.data"。