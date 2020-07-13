# replaytask，replay所需要的所有数据结构

# import marshmallow_dataclass
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class ReplayTestCase:
    testNumber: int
    ctestNumber: int
    fileContent: str

@dataclass
class ReplayRequest:
    apkName: str  # with ".apk" in the end
    packageName: str # only the package name
    androidVersion: str # version to run on
    replayCaseList: List[ReplayTestCase]
    desiredCaps: Dict


@dataclass
class ReplayTestCaseSummary:
    apkName: str  # with ".apk" in the end
    packageName: str # only the package name
    androidVersion: str # version to run on
    testNumber: int
    ctestNumber: int
    writeName: str


@dataclass
class ReplayResponse:
    success: bool
    errorMessage: str
    pageSource: str
    imgBase64: str
    adbLog: str
    testcaseSummary: ReplayTestCaseSummary