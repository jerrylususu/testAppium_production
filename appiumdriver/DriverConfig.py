def config():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '9'
    desired_caps['deviceName'] = 'emulator-5554'
    desired_caps['appPackage'] = 'de.danoeh.antennapod'
    desired_caps['appActivity'] = 'de.danoeh.antennapod.activity.SplashActivity'
    desired_caps['eventTimings'] = True
    desired_caps['automationName'] = 'UIAutomator2'
    return desired_caps

