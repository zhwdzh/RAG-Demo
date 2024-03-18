# 前置需求
[Ollama](https://ollama.com/)和[Text Embeddings Inference](https://huggingface.co/docs/text-embeddings-inference/index)，前者用于部署LLM，后者用于嵌入模型和重排模型，具体可以根据实际的部署环境进行替换。

向量数据库选用了[Qdrant](https://qdrant.tech/documentation/quick-start/)，可以通过Docker快速启动，或者使用in-memory模式进行调试

# 依赖安装
推荐使用[uv](https://github.com/astral-sh/uv)进行依赖安装
```shell
uv venv
source .venv/bin/activate
uv pip sync requirements.txt
```

# 框架和使用说明
将转换为txt的文档放置于`data`目录下，并将`question.jsonl`也放置在`data`目录下，其文件结构如下
```shell
> tree -L 3 -d data/
data/
└── output
    ├── director
    │   ├── License申请操作指南
    │   ├── TCF部署TECS Director
    │   ├── nodes
    │   ├── 备份
    │   ├── 安全
    │   ├── 容灾
    │   ├── 性能FTP北向接口规范
    │   ├── 日志FTP北向接口规范
    │   ├── 告警SNMP北向接口规范
    │   ├── 产品描述
    │   ├── 例行维护
    │   ├── 对接指南
    │   ├── 操作指南
    │   ├── 故障处理
    │   ├── 硬件配置
    │   ├── 配置指南
    │   ├── 文档包简介
    │   ├── 性能指标参考
    │   ├── 租户操作指南
    │   ├── 隐私保护声明
    │   ├── 中兴云操作指南
    │   ├── 告警与通知处理
    │   ├── 性能计数器参考
    │   ├── 端口和服务清单
    │   └── 技术服务使用指南
    └── rcp
        ├── CommonS_HTTP_LB
        ├── CommonS_IPS
        ├── CommonS_OAM
        ├── CommonS_SIG
        ├── CommonS_TMSP
        ├── Namf
        ├── Nausf
        ├── Nbsf
        ├── Nchf
        ├── Ncudr_Access
        ├── Ncudr_AccessManagement
        ├── Ncudr_SystemManagement
        ├── Nnrf
        ├── Nnssf
        ├── Npcf
        ├── Npcf_LOG
        ├── Npcf_LogStoreUnit
        ├── Npcf_PolicyManagement
        ├── Npcf_SIGLB
        ├── Npcf_SMPolicyControl
        ├── Npcf_SystemManagement
        ├── Nsmf
        ├── Nsmsf
        ├── Nudm
        ├── ZUF-59-55-051 VoNR
        └── nodes

55 directories
```
将`.env.example`复制为`.env`并修改相应设置，然后运行
```shell
python main.py
```
第一次运行会进行文档的切块和嵌入，时间较久，后续过程如果需要重新嵌入，可以设置`reindex=True`

生成的答案会放置在`data/my_answers.jsonl`
