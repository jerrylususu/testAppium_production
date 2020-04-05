import collections

import apkutils


def analyse_apk(path):
    apk = apkutils.APK(path)

    manifest = apk.get_manifest()
    activities = manifest['application']['activity']
    main_activity = ''
    for activity in activities:
        if 'intent-filter' in activity.keys():
            intent_filters = activity['intent-filter']
            if type(intent_filters) is collections.OrderedDict:
                if intent_filters['action']['@android:name'] == 'android.intent.action.MAIN':
                    main_activity = activity['@android:name']
            else:
                for intent_filter in intent_filters:
                    if intent_filter['action']['@android:name'] == 'android.intent.action.MAIN':
                        main_activity = activity['@android:name']

    package = apk.get_manifest()['@package']
    SDKversion = apk.get_manifest()['@android:compileSdkVersionCodename']

    return SDKversion, package, main_activity