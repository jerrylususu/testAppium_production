from analyseapk.AnalyseAPK import analyse_apk

apk_path="/home/luzhirui/jerrylu/testAppium/0406apks/us.mitene.apk"

SDKversion, package, main_activity, minSdk = analyse_apk(apk_path)

print(SDKversion)
print(package)
print(main_activity)
print(minSdk)