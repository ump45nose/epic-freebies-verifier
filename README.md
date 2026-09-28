# Epic 免费游戏领取状态核验适配器

这是 [Autsunset/epic-free](https://github.com/Autsunset/epic-free) 运行流程的独立覆盖层，保留其登录和领取能力，并在订单历史返回非 JSON 或无法确认时，到已登录的 Epic 商品页逐一读取精确的 `In Library` 状态。只有所有待确认商品都显示该状态、且没有明确领取失败，才报告成功；单纯按钮不可点不算拥有游戏。

## 构建和执行

运行时依赖上游代码和模型配置，仓库不复制它们。此覆盖层在上游 `Ronchy2000/epic-freebies-helper` 的 `d90190b` 版本及 `Autsunset/epic-free` 的镜像 revision `3d3d30a` 组合上做过适配。先在本仓库下准备上游源码：

```bash
git clone https://github.com/Ronchy2000/epic-freebies-helper.git upstream
git -C upstream checkout d90190b
cp .env.example .env
# 在本机填写 .env 后构建；不要提交 .env。
docker compose -f compose.example.yaml build
docker compose -f compose.example.yaml run --rm epic-helper
```

运行结果保存在 `./data/claim-result.json`。只有 `success=true` 且 `verification=storefront-library` 或可确认的订单历史，才视为完成。配置外部定时器按周或按日调用上述一次性容器即可；脚本不会自动兑换付费商品。`worker.py` 是可选的文件队列入口，需要另行挂载私有 `/queue`。

## 数据与来源

账号密码、模型密钥、浏览器会话、截图和订单记录均留在本地 `./data` 或 `.env`，已被 Git 忽略。本覆盖层依赖 GPL-3.0 上游，按相同许可证发布；可在 [Autsunset/epic-free](https://github.com/Autsunset/epic-free) 和 [Ronchy2000/epic-freebies-helper](https://github.com/Ronchy2000/epic-freebies-helper) 查看原项目与完整安装要求。这里的商品页核验是独立补充，不能替代 Epic 账号的实际订单核查。
