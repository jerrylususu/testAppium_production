import os
import sys

# 生成 task

local_status_file = "status"

with open(local_status_file, "w") as f:
    
    for i in range(0, int(1e8), int(1e7) ):
        print(i)
        f.write(str(i) + "\n")

