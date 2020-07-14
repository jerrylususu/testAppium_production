from analyseapk.AnalyseAPK import analyse_apk
from pathlib import Path

base_apk_root=Path("/home/luzhirui/fdroid_1k6/")
apk_file="/home/luzhirui/jerrylu/ui_research/fdroid_1k6_step234/fdroid_1k6_gator_success.txt"

if __name__ == "__main__":
    lines = []
    with open(apk_file, "r") as f:
        lines = f.readlines()
    
    apk_file_root = Path(apk_file).parent
    with open(apk_file_root / "apk_version_output.txt", "w") as f2:
        for line in lines:
            print(line)
            apk = base_apk_root / f"{line}.apk"
            SDKversion, package, main_activity, minSdk = apk(apk_path)
            print(f"SDKversion, package, main_activity, minSdk: {(SDKversion, package, main_activity, minSdk)}")
            f2.write(SDKversion)
            f2.write("\n")