import os
import re
from pathlib import Path
from datetime import datetime

def rename_mp4_files(root_dir: str, prefix: str):
    root = Path(root_dir)

    # 判断是否已经是目标格式：prefix_YYYYMMDD_HHMMSS(_n).mp4
    pattern = re.compile(rf"^{re.escape(prefix)}_\d{{8}}_\d{{6}}(_\d+)?\.mp4$", re.IGNORECASE)

    for file in root.rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() != ".mp4":
            continue

        # ✅ 如果已经是目标格式，直接跳过
        if pattern.match(file.name):
            continue

        # 获取创建时间（ctime）
        ctime = file.stat().st_ctime
        dt = datetime.fromtimestamp(ctime)
        time_str = dt.strftime("%Y%m%d_%H%M%S")

        # 生成新文件名
        new_name = f"{prefix}_{time_str}.mp4"
        new_path = file.with_name(new_name)

        # 避免重名覆盖
        counter = 1
        while new_path.exists():
            new_name = f"{prefix}_{time_str}_{counter}.mp4"
            new_path = file.with_name(new_name)
            counter += 1

        # 重命名
        file.rename(new_path)
        print(f"Renamed: {file} -> {new_path}")


if __name__ == "__main__":
    target_dir = r"D:\your\folder"  # 修改为目标目录
    prefix = "video"               # 修改为你的前缀

    rename_mp4_files(target_dir, prefix)