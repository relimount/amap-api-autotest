# amap-api-autotest

高德开放平台 Web 服务接口自动化测试框架 · Python + pytest + requests

**91 条用例 · 全量执行 23 秒 · 全绿**

**[查看在线 Allure 报告 →](https://relimount.github.io/amap-api-autotest/)**

---

## 它测什么

覆盖高德开放平台 7 个 Web 服务接口：地理编码、逆地理编码、天气、驾车 / 步行 / 骑行 / 公交路径规划。

用例构成：

| 类型 | 数量 | 说明 |
|---|---|---|
| 接口用例 | 53 | YAML 声明，正向 + 异常并重 |
| 串联链路 | 1 | 地理编码 → 驾车导航，验证跨接口数据流转 |
| 断言引擎单测 | 37 | 不依赖网络，秒级回归 |
| **合计** | **91** | |

## 架构

| 层 | 职责 |
|---|---|
| `api/` | 接口封装，一个类管一组接口，统一注入 key 与超时 |
| `testcases/` | YAML 用例，声明请求参数与期望值 |
| `tests/` | 测试入口，只做参数化转发 |
| `assert_util.py` | 声明式断言引擎 |
| `utils/` | 令牌桶限流 |

**文件名即契约**：`tests/test_weather.py` 自动加载 `testcases/weather.yaml`，由 `conftest.py` 里的 `pytest_generate_tests` 在收集阶段完成映射与展开。测试函数只要在签名里声明 `case` 参数就自动参数化，没声明的（如导航链路、引擎单测）原样执行。

## 快速开始

```bash
# 1. 装依赖（uv 会自动拉取项目声明的 Python 版本）
uv sync

# 2. 配 key：在项目根目录新建 .env
#    AMAP_KEY=你的key

# 3. 跑全量
uv run pytest -q

# 4. 看报告
allure serve report
```

## 加用例

一条用例就是一个 YAML 块，不需要写 Python：

```yaml
- case: 缺 origin
  params:
    destination: 116.434446,39.90816
  expect:
    http_status: 200
    body:
      status: "0"
      info: MISSING_REQUIRED_PARAMS
      infocode: "20001"
    not_has_keys:
      - count
      - route
```

- **加一条用例**：往对应 YAML 的 `cases` 里加一个块，完
- **加一个接口**：`api/` 加一个方法 → `testcases/` 加一份同名 YAML → `tests/` 加三行入口

## 断言引擎

支持 5 类校验：`http_status`、`body`（按路径精确匹配）、`has_keys`、`not_has_keys`、`types`（类型校验）。

字段路径支持点号分层与列表下标，例如 `route.paths.0.steps.0.instruction`。

针对「假绿」做了三个设计：

| 设计 | 解决什么 |
|---|---|
| 哨兵值 | 字段缺失返回 `_MISSING` 而非 `None`，避免「字段不存在」被当成「值为 null」放行 |
| 未知键报错 | `expect` 里出现拼错的键（如 `haskey`）直接抛错，不会静默跳过整段断言 |
| bool / int 分离 | `isinstance(True, int)` 为 `True`，所以 `int` 校验显式排除 `bool` |

前两条都有对应的回归用例。引擎自身 37 条单测，不依赖网络。

## 限流

开放平台按 key 计 QPS，超限返回 `CUQPS_HAS_EXCEEDED_THE_LIMIT`。

`utils/ratelimit.py` 实现令牌桶，通过 `conftest.py` 的 autouse fixture 挂在每条用例执行前。阈值由环境变量 `AMAP_QPS` 注入，默认 2.5——实测 3 以上会偶发超限，所以留了余量。

## CI

`Jenkinsfile`：每日定时执行（Jenkins 服务器时区 08:00），key 走 Jenkins Credentials，结果归档为 Allure 报告，构建失败邮件告警。`AMAP_QPS` 作为流水线参数暴露，出问题时可以不改代码直接降速。