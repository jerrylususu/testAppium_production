import os
from time import sleep
from datetime import datetime
import subprocess

apk_path="/home/luzhirui/jerrylu/ui_research/DeepIntent/IconWidgetAnalysis/RunInputs/Apks/de.danoeh.antennapod.apk"
aapt_path="/home/luzhirui/jerrylu/android9/android-9/aapt"

return_str =subprocess.check_output([aapt_path,"dump","badging", apk_path])
decode_li = return_str.decode("utf8").split("\n")
package = decode_li[0].replace("'","").split(" ")[1].replace("name=","")
for line in decode_li:
    if line.startswith("sdkVersion:"):
        minSdk = int(line.replace("'","").split(":")[1])
    if line.startswith("targetSdkVersion:"):
        SDKversion = int(line.replace("'","").split(":")[1])
    if line.startswith("launchable-activity"):
        main_activity = line.split(" ")[1].replace("'","").replace("name=","")
print(SDKversion, package, main_activity, minSdk)
# main_activity = "wsj.ui.IssueActivity"