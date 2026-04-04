# JobSpy API

LinkedIn 职位搜索 REST API 服务。

## 技术栈

- Python + FastAPI + Uvicorn
- python-jobspy (LinkedIn 职位爬取)

## 项目结构

- `main.py` — FastAPI 应用 (健康检查 + 职位搜索端点)
- `requirements.txt` — 依赖定义
- `Procfile` — Railway/Heroku 部署配置

## 开发命令

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## API 端点

- `GET /health` — 健康检查
- `GET /jobs?query=...&location=...` — 职位搜索 (支持薪资范围、距离等参数)

## 部署

- 通过 Procfile 部署到 Railway: `uvicorn main:app --host 0.0.0.0 --port $PORT`
