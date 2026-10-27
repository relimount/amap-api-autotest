from api.direction import DirectionAPI
from api.geocode import GeocodeAPI

address1 = "成都师范学院温江校区"
address2 = "天府软件园"
location1 = '103.828894,30.676067'

geo = GeocodeAPI()
direction = DirectionAPI()

def _to_code(address):
    body = geo.get_geocode(address).json()
    assert body['status'] == '1', "导航测试: 地理编码失败"
    return body['geocodes'][0]['location']


def test_navigate_driving_address_to_address():
    """测试地址到地址的驾驶导航"""
    begin = _to_code(address1)
    end = _to_code(address2)
    body = direction.get_driving(begin, end).json()
    assert body['status'] == '1', "导航测试: 驾驶导航失败"
    assert body['route']['paths'][0], "导航测试: 驾驶导航无步骤"