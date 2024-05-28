import os


def get_pdf_file(directory):
    # 获取目录下的所有文件
    files = os.listdir(directory)

    # 筛选出以.pdf结尾的文件
    pdf_files = [file for file in files if file.endswith('.pdf')]

    # 检查筛选出的文件数量
    if len(pdf_files) > 1:
        raise Exception("More than one PDF file found in the directory.")
    elif len(pdf_files) == 0:
        # raise Exception("No PDF file found in the directory.")
        return None
    # 返回文件的完整路径
    return os.path.join(directory, pdf_files[0])


def get_md_file(directory):
    files = os.listdir(directory)
    md_files = [file for file in files if file.endswith('.md')]
    if len(md_files) > 1:
        raise Exception("More than one Markdown file found in the directory.")
    elif len(md_files) == 0:
        # raise Exception("No Markdown file found in the directory.")
        return None
    return os.path.join(directory, md_files[0])


def get_docx_file(directory):
    files = os.listdir(directory)
    docx_files = [file for file in files if file.endswith('.docx')]
    if len(docx_files) > 1:
        raise Exception("More than one Docx file found in the directory.")
    elif len(docx_files) == 0:
        # raise Exception("No Docx file found in the directory.")
        return None
    return os.path.join(directory, docx_files[0])