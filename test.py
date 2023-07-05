import sys
import time

def print_progress_bar(iteration, total, bar_length=50):
    percent = "{:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    sys.stdout.write(f"\r[{bar}] {percent}%")
    sys.stdout.flush()

# 示例：模拟一个长时间任务
total_iterations = 100
for i in range(total_iterations):
    # 模拟任务处理时间
    time.sleep(0.1)
    print_progress_bar(i + 1, total_iterations)

print("\n任务完成！")
