# Transcript2vioce

## 这是一个使用阿里云语音合成服务进行批量生成的脚本

Transcript2vioce.py是主程序。

该程序只在window下以python3.10版本进行测试，暂时没有GUI，只能使用CLI调用。

很抱歉程序中基本上没有注释。

#### 使用方式为：

首先你需要申请阿里云语音合成试用，并通过`pip install aliyun-python-sdk-core==2.13.3`安装`aliyunsdkcore`。

然后请在`./config.json`文件中修改配置，具体内容如下：

```json
{
    "AccessKeyId": "",				#aliyun分配的AccessKeyID
    "AccessKeySecret": "",			#aliyun分配的AccessKeySecret
    "appkey": "",					#aliyun上的项目appkey
    "voice": "",					#发音人的拼音，使用random随机选择发音人
    "format": "",					#输出格式，仅限PCM、MP3、WAV
    "sample_rate": 16000,			#码率，仅限8000、16000，建议16000
    "volume": 50,					#声音大小
    "speech_rate": 0,				#语速
    "pitch_rate": 0					#语调
}
```

你可以使用`-c`来改变配置文件的路径，默认为`./config.json`。

当你准备好环境配置的时候，通过一下格式运行：

```Transcript2vioce.py [-h|--help|args] ```

例如你的输入文件为 input.txt，通过：

```Transcript2vioce.py input.txt```

来运行，默认输出位置是程序根目录下的`./output`文件夹中，程序会根据发音人的不同创建次级文件夹，可以用`-o`选项来改变默认输出路径。

程序会自动跳过已经生成的文件，除非你添加`-f`选项，这将强制重新生成并覆盖。

试用版的语音合成只支持2发并行，这也是默认线程数，如果你开通了商用版，可以使用`-t`来改变线程数。

如果你是使用阿里云上海内网服务器运行，请添加`-i`选项来选用内网，这将提高速度并节省公网开销。

#### 输入格式

输入文件的格式应当为`语音名（纯英文数字下划线） 语音内容（纯中文） `，例如：

```
a_1 这是一段测试语音
a_2 这是输入文件的标准格式
```

你可以使用我提供的`txt2transcript.py`脚本进行预处理，它会将再自己目录下的所有txt文本切割成短句并导出标准格式的文件，它将直接去除所有标点与英文以及语气词，并将数字转化为汉字写法，但它需要pypinyin，请使用`pip install pypinyin`安装，生成的文件可以直接用于数据集。

# 使用GPLv2发布

这个程序暂时还不是很完善的状态，欢迎大家的补全。



