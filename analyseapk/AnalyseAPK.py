import re

import apkutils


def analyse_apk(path):
    apk = apkutils.APK(path)

    manifest_string = apk.get_mini_mani()
    main_activity = None
    ptn = r'<activity .*?android:name="([^"]*?)"[^<>]*?>.*?<action android:name="android.intent.action.MAIN">.*?</activity>'
    result = re.search(ptn, manifest_string)
    if result:
        main_activity = result.groups()[0]

    manifest = apk.get_manifest()
    package = apk.get_manifest()['@package']
    uses_sdk = manifest['uses-sdk']
    minSdk = uses_sdk.get('@android:minSdkVersion', '')
    targetSdk = uses_sdk.get('@android:targetSdkVersion', '')

    return targetSdk, package, main_activity, minSdk