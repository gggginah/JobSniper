import sys

def get_stage2_folder_from_args():
    if "--stage2" in sys.argv:
        index = sys.argv.index("--stage2")

        if index + 1 >= len(sys.argv):
            raise ValueError("请在 --stage2 后面提供 output 文件夹路径。")

        return sys.argv[index + 1]

    return None



def get_export_docx_folder_from_args():
    if "--export-docx" in sys.argv:
        index = sys.argv.index("--export-docx")

        if index + 1 >= len(sys.argv):
            raise ValueError("请在 --export-docx 后面提供 output 文件夹路径。")

        return sys.argv[index + 1]

    return None

