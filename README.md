# 🐾 BuddyFinder

Claude Code 宠物查找器。使用 Bun.hash 算法精确搜索，获得想要的任意属性组合的宠物。

## 安装

```bash
# 安装 Bun（必需）
curl -fsSL https://bun.sh/install | bash
```

## 使用

```bash
python3 buddy.py
```

选择宠物属性 → 点「🚀 开始搜索」→ 等结果 → 点「📋 复制 UID」

## 应用到 Claude Code

### 1. 编辑配置文件

```bash
nano ~/.claude.json
```

### 2. 在最上面添加 userID

```json
{
  "userID": "你复制的UID",
  "oauth": {...}
}
```

⚠️ **注意**：JSON 格式必须正确（注意逗号和引号）

### 3. 保存并重启 Claude Code

- macOS: ⌘Q（完全退出，不只是关闭窗口）
- 然后重新打开

### 4. 运行 `/buddy` 获得新宠物

## 搜索技巧

| 条件 | 成功率 | 耗时 |
|------|--------|------|
| `legendary penguin` | 1/100 | 秒内 ✅ |
| `legendary penguin + hat` | 1/1200 | 几秒 |
| `legendary penguin + shiny` | 1/10000 | 1-2 分钟 |

**策略**：先搜物种+稀有度，再加其他条件。

## 文件

| 文件 | 说明 |
|------|------|
| `buddy.py` | 主程序（GUI） |
| `buddy-finder-bun.js` | 搜索引擎 |
| `README.md` | 本文件 |

## 常见问题

**Q: 为什么搜索很慢？**  
A: 条件太严格。移除眼睛/闪光条件，或改成更常见的稀有度。

**Q: 改了配置没效果？**  
A: 检查清单：
- JSON 格式正确吗？（可用 `plutil -lint ~/.claude.json` 检查）
- 是否**完全退出** Claude Code？（⌘Q，不是关闭窗口）
- UID 是否正确复制？（应该 64 字符）

**Q: 能用 Node.js 代替 Bun 吗？**  
A: 不行。Bun.hash() 和 Node.js crypto 算法不同，会得到错误的宠物。

## 致谢

感谢 Linux DO 社区的逆向分析：https://linux.do/t/topic/1871870

---

**祝你找到完美的宠物！** 🎉
