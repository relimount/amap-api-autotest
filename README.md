# amap-api-autotest
高德开放平台 Web 服务接口自动化测试

## 技术栈
pytest · requests · PyYAML · Allure · Jenkins

## 快速开始
1. 建虚拟环境并装依赖
   python -m venv .venv && .venv\Scripts\activate
   pip install -r requirements.txt
2. 配 key（在项目根目录新建 .env）
   AMAP_KEY=你的高德key
3. 跑
   pytest -q                       # 全量
   pytest -m smoke -q              # 冒烟（P1 之后有）

## 目录结构
api/        接口封装层，一个类管一组接口，统一注入 key
testcases/  YAML 用例，新增用例不用写代码
tests/      测试入口，只做参数化转发
assert_util.py  断言解释器