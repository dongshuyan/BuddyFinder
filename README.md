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

### ⚠️ 第 0 步：备份配置文件

**强烈建议先备份**，以防万一：

```bash
cp ~/.claude.json ~/.claude.json.backup
```

### 1. 编辑配置文件

```bash
nano ~/.claude.json
```

### 2. 删除 companion 字段（重要！）

找到并删除以下内容：

```json
"companion": {
  "name": "...",
  "personality": "...",
  "hatchedAt": ...
}
```

删完后的文件应该看起来像：

```json
{
  "userID": "...",
  "oauth": {...},
  ...
  // companion 字段已删除
}
```

### 3. 添加新的 userID

把刷到的 UID 写进去，**替换原来的 userID**：

```json
{
  "userID": "你复制的UID",
  "oauth": {...}
}
```

✅ **完整示例：**

```json
{
  "userID": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6",
  "oauth": {
    "accountUuid": "xxx"
  }
}
```

⚠️ **注意**：
- 确保 JSON 格式正确（逗号、引号要对）
- `companion` 字段必须删除
- 可用 `plutil -lint ~/.claude.json` 验证格式

### 4. 保存并重启 Claude Code

- macOS: ⌘Q（完全退出，不只是关闭窗口）
- Windows: 完全关闭应用
- 然后重新打开

### 5. 运行 `/buddy` 获得新宠物

在对话中输入：

```
/buddy
```

你会看到新宠物！✨

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
