import cv2 as cv
from pathlib import Path
import json
import re
from tqdm import tqdm
import xml.dom.minidom
from xml.etree import ElementTree
import xmltodict,json
from xmldiff import main
from lxml import etree
import difflib as df

import warnings
import sys

import logging
LOG_FORMAT = "%(levelname)s: %(asctime)s - [%(filename)s:%(lineno)s] - %(message)s"
# LOG_FORMAT = "%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s"
# logging.basicConfig(filename="pylogs/replay_analysis.log",level=logging.DEBUG, format=LOG_FORMAT)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

pg_parse_regex = re.compile("page_source_testcase_(.+)-insted_ctest_(\d+)_test(\d+)_budtmo_docker-android-x86-(.+)")
ss_parse_regex = re.compile("testcase_(.+)-insted_ctest_(\d+)_test(\d+)_budtmo_docker-android-x86-(.+)")

path = '/home/luzhirui/jerrylu/testAppium/replay_evo2/replay_page_sources'
page_source_dir = Path(path)

path = '/home/luzhirui/jerrylu/testAppium/replay_evo2/replay_screenshots'
ss_source_dir = Path(path)

output_dir = Path("/home/luzhirui/jerrylu/testAppium/replay_evo2/replay_compare")

def traverse(root, taglist):
    t = root.tag
    t = t.replace('android.widget.', '')
    taglist.append(t)
    items = dict(root.items())
    children = root.getchildren()
    for c in children:
        traverse(c, taglist)

def removebounds(root):
    for rank in root.iter('bounds'):
        del rank.attrib['bounds']
    children = root.getchildren()
    for c in children:
        removebounds(c)

def apk_task_pg(apk_name, apk_dict):
    all_compare_list = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") 
        layer1_dict = apk_dict[apk_name]
        for test, layer2_dict in layer1_dict.items():
            split_li = layer2_dict

            xml_list = list(split_li.values())
            sequence = []
            json_l = []
            tag = []
            tag_string = []

            for i in xml_list:
                with open(i, "r") as f:
                    a = f.read()
                    sequence.append(a)
                    root = ElementTree.fromstring(a)
                    taglist = []
                    traverse(root, taglist)
                    tag.append(taglist)
                    string = xmltodict.parse(a)
                    json_l.append(json.dumps(string))

            for i in tag:
                string = ''
                for item in i:
                    string += item
                tag_string.append(string)


            for i in range(len(sequence)):
                for j in range(i+1, len(sequence)):
                    results_dict = {}
                    apk_name, ctest_no, test_no, android_ver1 = re.match(pg_parse_regex,xml_list[i].stem).groups()
                    apk_name, ctest_no, test_no, android_ver2 = re.match(pg_parse_regex,xml_list[j].stem).groups()
                    results_dict["apk_name"] = apk_name
                    results_dict["ctest_no"] = ctest_no
                    results_dict["test_no"] = test_no
                    results_dict["android_ver1"] = android_ver1
                    results_dict["android_ver2"] = android_ver2
            #         results_dict["compare_target"] = str(xml_list[i])+","+str(xml_list[j])
                    ts = df.SequenceMatcher(None, sequence[i], sequence[j])
                    results_dict["1a_text"] = ts.ratio()
                    s = df.SequenceMatcher(None, json_l[i], json_l[j])
                    r = s.ratio()
                    results_dict["1b_json"] = r
                    tss = df.SequenceMatcher(None, tag_string[i], tag_string[j])
                    results_dict["1c_tag_string"] = tss.ratio()
                    tl = df.SequenceMatcher(None, tag[i], tag[j])
                    results_dict["1d_tag_list"] = tl.ratio()
    #                     file1 = str(xml_list[i])
    #                     file2 = str(xml_list[j])
    #                     ans = main.diff_files(file1,file2, diff_options={'F':0.5})
    #                     results_dict["2a_xml_compare"] = "same" if len(ans)==0 else "different"
    #                     first = ElementTree.parse(str(xml_list[i]))
    #                     right = ElementTree.parse(str(xml_list[j]))
    #                     removebounds(first.getroot())
    #                     removebounds(right.getroot())
    #                     first.write(tmp_path + 'output1.xml', encoding="utf-8", xml_declaration=True)
    #                     right.write(tmp_path + 'output2.xml', encoding="utf-8", xml_declaration=True)
    #                     ans = main.diff_files(tmp_path + 'output1.xml', tmp_path + 'output2.xml', diff_options={'F':0.5})
    #                     results_dict["2b_xml_notag_compare"] = "same" if len(ans)==0 else "different"
    #                     all_compare_list.append(results_dict)
    #                     print(results_dict)
                    all_compare_list.append(results_dict)
    return all_compare_list

def build_dict_xml(apk_name):
    apk_dict = {}
    file_list = list(page_source_dir.iterdir())
    for pg in tqdm(file_list):
        if pg.name.split(".")[-1] == "xml" and apk_name in pg.name:
            apk_name, ctest_no, test_no, android_ver = re.match(pg_parse_regex, pg.stem).groups()
            if apk_name not in apk_dict:
                apk_dict[apk_name] = {}
            current_layer1_dict = apk_dict[apk_name]
            test_name = f"c{ctest_no}_t{test_no}"
            if test_name not in current_layer1_dict:
                current_layer1_dict[test_name] = {}
            current_layer2_dict = current_layer1_dict[test_name]
            current_layer2_dict[android_ver] = pg
    return apk_dict

def build_dict_png(apk_name):
    apk_dict = {}
    file_list = list(ss_source_dir.iterdir())
    for pg in tqdm(file_list):
        if pg.name.split(".")[-1] == "png"  and apk_name in pg.name:
            apk_name, ctest_no, test_no, android_ver = re.match(ss_parse_regex, pg.stem).groups()
            if apk_name not in apk_dict:
                apk_dict[apk_name] = {}
            current_layer1_dict = apk_dict[apk_name]
            test_name = f"c{ctest_no}_t{test_no}"
            if test_name not in current_layer1_dict:
                current_layer1_dict[test_name] = {}
            current_layer2_dict = current_layer1_dict[test_name]
            current_layer2_dict[android_ver] = pg
    return apk_dict

def apk_task_ss(apk_name, apk_dict):
    all_compare_dict = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore") 
        try:
            layer1_dict = apk_dict[apk_name]
        except KeyError:
            return all_compare_dict
        for test, layer2_dict in layer1_dict.items():
            split_li = layer2_dict
            li = compare_multi_images(list(split_li.values()))
            all_compare_dict[test] = li
    return all_compare_dict

def compare_images(path1, path2):
    path1 = str(path1)
    path2 = str(path2)
    src_base = cv.imread(path1)
    src_test1 = cv.imread(path2)

    res_dict = {}


    if src_base is None or src_test1 is None :
        print('Could not open or find the images!', path1, path2)
        # exit(0)
        res_dict["base_base"] = -1 # 标准，一般是0
        res_dict["base_half"] = -1 # 替代的一个值？
        res_dict["base_test1"] = -1 # 比较结果
        return res_dict
    hsv_base = cv.cvtColor(src_base, cv.COLOR_BGR2HSV)
    hsv_test1 = cv.cvtColor(src_test1, cv.COLOR_BGR2HSV)

    hsv_half_down = hsv_base[hsv_base.shape[0]//2:,:]
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges # concat lists
    # Use the 0-th and 1-st channels
    channels = [0, 1]
    hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    hist_half_down = cv.calcHist([hsv_half_down], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_half_down, hist_half_down, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
    hist_test1 = cv.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

    
    for compare_method in range(3,4):
        base_base = cv.compareHist(hist_base, hist_base, compare_method)
        base_half = cv.compareHist(hist_base, hist_half_down, compare_method)
        base_test1 = cv.compareHist(hist_base, hist_test1, compare_method)

        #print('Method:', compare_method, 'Perfect, Base-Half, Base-Test(1)',\
        #      base_base, '/', base_half, '/', base_test1)

        # print(base_base-)
        res_dict["base_base"] = base_base # 标准，一般是0
        res_dict["base_half"] = base_half # 替代的一个值？
        res_dict["base_test1"] = base_test1 # 比较结果
    return res_dict

def compare_multi_images(image_list):
    li = []
    for i in range(len(image_list)):
        for j in range(i+1, len(image_list)):
            ver1 = re.match(ss_parse_regex, image_list[i].stem).groups()[-1]
            ver2 = re.match(ss_parse_regex, image_list[j].stem).groups()[-1]
            res = compare_images(image_list[i], image_list[j])
            res["ver1"] = ver1
            res["ver2"] = ver2
            li.append(res)
    return li

if __name__ == "__main__":

    apk_name = sys.argv[1]
    apk_file = Path(apk_name)
    apk_name = apk_file.name
    # print("processing ", apk_name)

    # special skip for re-run
    output_ss = Path(output_dir / "{}-ss.json".format(apk_name))
    need_to_process = True
    if output_ss.exists():
        need_to_process = False

    # try:
    #     xml_dict = build_dict_xml(apk_name)
    #     pg_compare_res = apk_task_pg(apk_name, xml_dict)
    #     with open(output_dir / "{}-pg.json".format(apk_name), "w") as f:
    #         json.dump(pg_compare_res, f)
    # except Exception as e:
    #     logging.exception("xml")

    if need_to_process:
        print("working on {}".format(apk_name))
        try:
            png_dict = build_dict_png(apk_name)
            img_compare_res = apk_task_ss(apk_name, png_dict)
            with open(output_dir / "{}-ss.json".format(apk_name), "w") as f:
                json.dump(img_compare_res, f)
        except Exception as e:
            logging.exception("png")


    pass