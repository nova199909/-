import datetime


def generate_report(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"Report generated at {timestamp}\n\n"
    report += f"URL: {data[1]}\n"
    report += f"payload: {data[2]}\n"
    report += f"漏洞类型：{data[3]}\n"
    # 在这里可以根据需要将其他相关数据添加到报告中

    with open("report.txt", "a") as file:
        file.write(report)
        file.write("\n\n")
