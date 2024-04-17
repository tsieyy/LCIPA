"""
    用于将langgraph verbose生成的信息从stdin重定向至streamlit进行显示
"""

import sys
import contextlib
import emoji

class StreamlitWriter:
    def __init__(self, st, container):
        self.st = st

    def write(self, s):
        # self.st.markdown(f'```\n{s}```')
        # self.st.write(s)
        if s and emoji.is_emoji(s[0]):
            self.st.write(s)

    def flush(self):
        pass


@contextlib.contextmanager
def redirect_stdout_to_streamlit(st, container=None):
    original_stdout = sys.stdout
    sys.stdout = StreamlitWriter(st, container)
    try:
        yield
    finally:
        sys.stdout = original_stdout