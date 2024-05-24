from datetime import datetime, timedelta
import json
import random
import requests
from hashlib import md5
import hashlib
import urllib.parse
from geopy.distance import geodesic

input_value = True
phone = ""
password = ""
token = ""
run_distance = 0  # 路程，单位为米
run_time = 0  # 时间，单位为分钟
app_key = "389885588s0648fa"


class AppConfig:
    def __init__(self):
        self.app_version = "1.8.0"  # APP版本，一般不做修改
        self.brand = ""  # 手机品牌
        self.mobile_type = ""  # 型号
        self.sys_version = "10"  # 系统版本
        self.device_token = ""
        self.device_type = "1"

        
config = AppConfig()

class NewRecordBody:
    def __init__(self):
        self.againRunStatus = "0"
        self.againRunTime = 0
        self.appVersions = "1.8.0"
        self.brand = None
        self.mobileType = None
        self.sysVersions = None
        self.trackPoints = None
        self.distanceTimeStatus = "1"
        self.innerSchool = "1"
        self.runDistance = 0
        self.runTime = 0
        self.userId = 0
        self.vocalStatus = "1"
        self.yearSemester = None
        self.recordDate = None
        self.realityTrackPoints = None

class Location:
    def __init__(self):
        self.id = 0
        self.location = ""
        self.edge = []

class SchoolBound:
    def __init__(self):
        self.siteName = None
        self.siteBound = None
        self.boundCenter = None


class RunStandard:
    def __init__(self):
        self.standardId = 0
        self.schoolId = 0
        self.boyOnceTimeMin = 0
        self.boyOnceTimeMax = 0
        self.semesterYear = None

# import random
# import json
# from datetime import datetime, timedelta
# from geopy.distance import geodesic

import random
from datetime import datetime, timedelta
import json
from geopy.distance import geodesic

class TrackUtils:
    @staticmethod
    def gen(distance, locations):
        current_distance = 0
        start_location_index = random.randint(0, len(locations) - 1)
        start_location = locations[start_location_index]
        current_location = start_location
        result = []
        last_edge_index = [0, 0]

        start_time = datetime.now() - timedelta(minutes=30)

        # 起始位置
        current = current_location['location'].split(",")
        result.append(f"{current[0]}-{current[1]}-{start_time}-{TrackUtils.rand_accuracy()}")

        while current_distance < distance:
            current = current_location['location'].split(",")
            edge = current_location['edge']

            if not edge:
                print("edge为空")

            rand_index = random.randint(0, len(edge) - 1)
            if edge[rand_index] == last_edge_index[0]:
                if len(edge) == 1:
                    pass
                else:
                    rand_index = (rand_index + 1) % len(edge)

            last_edge_index[0], last_edge_index[1] = last_edge_index[1], edge[rand_index]
            next_index = edge[rand_index]

            if next_index == -1:
                next_index = edge[(rand_index + 1) % len(edge)]

            next_location = locations[next_index]
            start = list(map(float, current))

            # 增大路径宽度：将偏移量调整为较大的范围
            next_location_str = next_location['location'].split(",")
            offset = random.uniform(-1, 1) / 100000  # 这里将偏移范围增加至[-0.00001, 0.00001]
            next_location_str[0] = str(round(float(next_location_str[0]) + offset, 6))
            next_location_str[1] = str(round(float(next_location_str[1]) + offset, 6))

            end = list(map(float, next_location_str))

            go_distance = TrackUtils.calculate_distance(start, end)
            current_distance += go_distance

            # 在每两个大点之间生成更多小点
            for i in range(1, 11):  # 增加小点数量
                fraction = i / 10.0
                intermediate_point = TrackUtils.interpolate_point(start, end, fraction)
                # 在小点上添加更小的随机偏移
                intermediate_point[0] += random.uniform(-0.00001, 0.00001)
                intermediate_point[1] += random.uniform(-0.00001, 0.00001)
                distance_1 = TrackUtils.calculate_distance(start, intermediate_point)
                start_time += timedelta(milliseconds=int(distance_1 / random.randint(1, 5) * 1000))
                result.append(f"{intermediate_point[0]}-{intermediate_point[1]}-{start_time}-{TrackUtils.rand_accuracy()}")

            current_location = next_location

        start_time += timedelta(milliseconds=random.randint(5, 10) * 1000)
        result.append(f"{current_location['location'].replace(',', '-')}-{start_time}-{TrackUtils.rand_accuracy()}")
        return json.dumps(result)

    @staticmethod
    def rand_int(start, end):
        return random.randint(start, end - 1)

    @staticmethod
    def calculate_distance(start, end):
        return geodesic((start[1], start[0]), (end[1], end[0])).meters

    @staticmethod
    def interpolate_point(start, end, fraction):
        """计算起点和终点的插值

        Args:
            start (float, float): 起点坐标
            end (float, float): 终点坐标
            fraction (float): 插值比例

        Returns:
            [float, float]: 插值坐标
        """
        return [
            start[0] + (end[0] - start[0]) * fraction,
            start[1] + (end[1] - start[1]) * fraction
        ]

    @staticmethod
    def rand_accuracy():
        return 10 * random.random()


    

def generate_sign(query, body):
    if query is None:
        query = {}

    # 构建待签名字符串
    sb = []
    APPKEY = "389885588s0648fa";
    APPSECRET = "56E39A1658455588885690425C0FD16055A21676";
    # 将 query 中的参数按字典序排列
    sorted_keys = sorted(query.keys())
    for key in sorted_keys:
        value = query[key]
        if value is not None:
            sb.append(key)
            sb.append(value)

    # 追加 APPKEY 和 APPSECRET
    sb.append(APPKEY)
    sb.append(APPSECRET)

    if body is not None:
        sb.append(body)

    # 构建待签名字符串
    sb_str = ''.join(sb)

    # 删除特殊字符并进行 URL 编码
    sb_str = sb_str.replace(" ", "").replace("~", "").replace("!", "").replace("(", "").replace(")", "").replace("'", "")
    sb_str = urllib.parse.quote(sb_str, safe='~')

    # 计算 MD5
    md5 = hashlib.md5()
    md5.update(sb_str.encode('utf-8'))
    encoded_md5 = md5.hexdigest().upper()

    # 追加 'encodeutf8' 并返回签名
    return encoded_md5 + "encodeutf8"


def login(phone, password):
    global token  # declaring token as a global variable inside the function


    pass_hash = md5(password.encode()).hexdigest()
    API = "https://run-lb.tanmasports.com/v1/auth/login/password"
    try:
        body = {
            "appVersion": config.app_version,
            "brand": config.brand,
            "deviceToken": config.device_token,
            "deviceType": config.device_type,
            "mobileType": config.mobile_type,
            "password": pass_hash,
            "sysVersion": config.sys_version,
            "userPhone": phone
        }

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "token": token,
            "appkey": app_key
        }

        body_str = json.dumps(body)
        sign = generate_sign(None, body_str)
        headers["sign"] = sign

        response = requests.post(API, headers=headers, json=body)
        response_json = response.json()

        if response_json["code"] == 10000:
            user_info = response_json["response"]
            token = user_info["oauthToken"]["token"]
            return response_json
        else:
            return response_json

    except Exception as e:
        # print(e)
        raise e

def getRunStandard(schoolId):
    API = f"https://run-lb.tanmasports.com/v1/unirun/query/runStandard?schoolId={schoolId}"
    try:
        headers = {
            "token": token,
            "appkey": app_key,
            "Content-Type": "application/json; charset=UTF-8"
        }
        params = {
            "schoolId": str(schoolId)
        }
        sign = generate_sign(params, None)  # 此处需要你实现SignUtils类的get方法
        headers["sign"] = sign

        response = requests.get(API, headers=headers)
        standardResponse = response.json()

        if standardResponse['code'] != 10000:
            raise RuntimeError(standardResponse['msg'])

        return standardResponse['response']
    except Exception as e:
        print(e)
        return None

def getSchoolBound(schoolId):
    API = f"https://run-lb.tanmasports.com/v1/unirun/querySchoolBound?schoolId={schoolId}"
    try:
        headers = {
            "token": token,
            "appkey": app_key,
            "Content-Type": "application/json; charset=UTF-8"
        }
        params = {
            "schoolId": str(schoolId)
        }
        sign = generate_sign(params, None)
        headers["sign"] = sign

        response = requests.get(API, headers=headers)
        schoolBoundResponse = response.json()

        if schoolBoundResponse['code'] != 10000:
            raise RuntimeError(schoolBoundResponse['msg'])

        return schoolBoundResponse['response']
    except Exception as e:
        print(e)
        return None
    
def record_new(body):
    API = "https://run-lb.tanmasports.com/v1/unirun/save/run/record/new"
    try:
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "token": token,
            "appkey": app_key
        }
        # Convert NewRecordBody object to dictionary
        body_dict = {
            "againRunStatus": body.againRunStatus,
            "againRunTime": body.againRunTime,
            "appVersions": body.appVersions,
            "brand": body.brand,
            "mobileType": body.mobileType,
            "sysVersions": body.sysVersions,
            "trackPoints": body.trackPoints,
            "distanceTimeStatus": body.distanceTimeStatus,
            "innerSchool": body.innerSchool,
            "runDistance": body.runDistance,
            "runTime": body.runTime,
            "userId": body.userId,
            "vocalStatus": body.vocalStatus,
            "yearSemester": body.yearSemester,
            "recordDate": body.recordDate,
            "realityTrackPoints": body.realityTrackPoints
        }
        # Assuming SignUtils.get() returns the signature
        sign = generate_sign(None, json.dumps(body_dict))
        headers["sign"] = sign
        response = requests.post(API, headers=headers, json=body_dict)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except Exception as e:
        print(e)
    return None


def genTack(distance, school_site):
    try:
        if school_site == 0:
            file_name = "map_konggang.json"
        else:
            file_name = "map_longquan.json"

        with open(f"resources\{file_name}", "r") as f:
            locations = json.load(f)
            if not locations:
                print("配置读取失败")
                return None
            return TrackUtils.gen(distance, locations)
    except Exception as e:
        print(e)
        return None

def auto_run_post(phone, password, run_distance, run_time, school_site):

    try:
        userInfoResponse = login(phone, password)
        # print(userInfoResponse)
        userInfo = userInfoResponse["response"]
        userId = userInfo["userId"]
        if userId != -1:
            runStandard = getRunStandard(userInfo["schoolId"])
            # print(runStandard)
            schoolBounds = getSchoolBound(userInfo["schoolId"])
            # print(schoolBounds)

            # 新增跑步数据
            recordBody = NewRecordBody()
            recordBody.userId = userId
            recordBody.appVersions = config.app_version
            recordBody.brand = config.brand
            recordBody.mobileType = config.mobile_type
            recordBody.sysVersions = config.sys_version
            recordBody.runDistance = run_distance
            recordBody.runTime = run_time
            recordBody.yearSemester = runStandard["semesterYear"]
            recordBody.realityTrackPoints = schoolBounds[school_site]["siteBound"] + "--"

            # 今天日期 年-月-日
            formatTime = datetime.now().strftime("%Y-%m-%d")
            recordBody.recordDate = formatTime

            # 生成跑步数据
            tack = genTack(run_distance, school_site)
            # print(tack)
            recordBody.trackPoints = tack

            # 发送数据
            result = record_new(recordBody)
            print(result)
            return result
        else:
            return userInfoResponse["msg"]

    except Exception as e:
        # print(e)
        # return str(e)
        raise e
    

def auto_run_post_add_track(phone, password, run_distance, run_time, school_site, track):

    try:
        userInfoResponse = login(phone, password)
        if userInfoResponse["code"] != 10000:
            return userInfoResponse
        # print(userInfoResponse)
        userInfo = userInfoResponse["response"]
        userId = userInfo["userId"]
        if userId != -1:
            runStandard = getRunStandard(userInfo["schoolId"])
            # print(runStandard)
            schoolBounds = getSchoolBound(userInfo["schoolId"])
            # print(schoolBounds)

            # 新增跑步数据
            recordBody = NewRecordBody()
            recordBody.userId = userId
            recordBody.appVersions = config.app_version
            recordBody.brand = config.brand
            recordBody.mobileType = config.mobile_type
            recordBody.sysVersions = config.sys_version
            recordBody.runDistance = run_distance
            recordBody.runTime = run_time
            recordBody.yearSemester = runStandard["semesterYear"]
            recordBody.realityTrackPoints = schoolBounds[school_site]["siteBound"] + "--"

            # 今天日期 年-月-日
            formatTime = datetime.now().strftime("%Y-%m-%d")
            recordBody.recordDate = formatTime

            # print(track)
            recordBody.trackPoints = track

            # 发送数据
            result = record_new(recordBody)
            print(result)
            return result
        else:
            return userInfoResponse["msg"]

    except Exception as e:
        # print(e)
        # return str(e)
        raise e

if __name__ == '__main__':
    phone = ""
    password = ""
    run_distance = 4698
    run_time = 42
    school_site = 0  # 0表示航空港，1表示龙泉
    
    auto_run_post(phone, password, run_distance, run_time, school_site)