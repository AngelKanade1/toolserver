import tkinter as tk
import datetime


def write_update_log():
    log_entry = entry.get()  # 获取输入框中的更新日志内容
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前日期与时间
    log_text = f"{current_time}: {log_entry}\n"  # 构建日志条目

    with open("updatelog.txt", "r+", encoding='utf-8') as file:
        content = file.read()
        file.seek(0, 0)  # 将文件指针移动到文件开头
        file.write(log_text + content)  # 将新的日志条目写入文件
    entry.delete(0, tk.END)  # 清空输入框内容


root = tk.Tk()
root.title("更新日志工具")

# 创建标签和输入框
label = tk.Label(root, text="输入更新日志:")
label.pack()
entry = tk.Entry(root, width=50)
entry.pack()

# 创建按钮
button = tk.Button(root, text="提交", command=write_update_log)
button.pack()

root.mainloop()
