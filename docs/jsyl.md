
## Docker部署方法

使用虽然docker相关文件已经准备好了,但是使用docker部署会出现[watchdog报错](https://discuss.streamlit.io/t/watchdog-error-when-running-streamlit-in-docker/26865),
可能需要将streamlit降级使用,如果需要使用docker进行部署,可以把`pyproject.toml`中的streamlit版本降低一些. 没有测试过可能还是会有问题.