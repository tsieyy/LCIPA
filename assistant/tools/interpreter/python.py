from typing import Annotated

from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.utilities import PythonREPL

python_repl_tool = PythonREPLTool()
python_repl = PythonREPL()


@tool
def python_repl(
        code: Annotated[str, "The python code to execute to generate your chart."]
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = python_repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"


