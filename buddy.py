#!/usr/bin/env python3
"""
Claude Code Buddy Finder GUI
使用 Bun 的 hash 算法，真实匹配 Claude Code 中的宠物生成
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import sys
import os
from pathlib import Path

# 检查 bun 是否安装
def check_bun():
    try:
        result = subprocess.run(['bun', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

class BuddyFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Claude Code 宠物查找器")
        self.root.geometry("900x700")
        self.root.configure(bg='#f8f9fc')

        # 检查 bun
        if not check_bun():
            messagebox.showerror(
                "Bun 未找到",
                "未检测到 Bun 环境。\n\n请先安装 Bun：\n  curl -fsSL https://bun.sh/install | bash"
            )

        self.buddy_script = Path(__file__).parent / 'buddy-finder-bun.js'
        self.running = False
        self.current_process = None

        self.setup_ui()

    def setup_ui(self):
        # 主容器
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # 标题
        title = ttk.Label(main_frame, text="🐾 Buddy 查找器", font=("Helvetica", 20, "bold"))
        title.pack(pady=(0, 6))

        subtitle = ttk.Label(main_frame, text="找到你想要的 Claude Code 宠物", foreground="gray")
        subtitle.pack(pady=(0, 12))

        # 左右分栏
        content = ttk.Frame(main_frame)
        content.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(content)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 12))

        right_frame = ttk.Frame(content)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 提示信息
        info_text = "💡 提示：条件越多越难找到。建议从「物种+稀有度」开始，再加其他条件"
        info_label = ttk.Label(main_frame, text=info_text, foreground="#d97706", wraplength=800)
        info_label.pack(pady=(0, 12))

        # ===== 左栏：筛选条件 =====
        self.setup_filters(left_frame)

        # ===== 右栏：日志和结果 =====
        self.setup_output(right_frame)

    def setup_filters(self, parent):
        filter_frame = ttk.LabelFrame(parent, text="筛选条件", padding=12)
        filter_frame.pack(fill=tk.BOTH, expand=True)

        # 物种
        ttk.Label(filter_frame, text="🦆 物种", font=("Helvetica", 9, "bold")).pack(anchor=tk.W, pady=(0, 4))
        self.species_var = tk.StringVar(value="any")
        species_list = [
            "任意",
            "鸭子 (duck)", "鹅 (goose)", "史莱姆 (blob)", "猫 (cat)", "龙 (dragon)",
            "章鱼 (octopus)", "猫头鹰 (owl)", "企鹅 (penguin)", "乌龟 (turtle)",
            "蜗牛 (snail)", "幽灵 (ghost)", "蝾螈 (axolotl)", "水豚 (capybara)",
            "仙人掌 (cactus)", "机器人 (robot)", "兔子 (rabbit)", "蘑菇 (mushroom)", "胖墩 (chonk)"
        ]
        species_map = {
            "任意": "any", "鸭子 (duck)": "duck", "鹅 (goose)": "goose", "史莱姆 (blob)": "blob",
            "猫 (cat)": "cat", "龙 (dragon)": "dragon", "章鱼 (octopus)": "octopus",
            "猫头鹰 (owl)": "owl", "企鹅 (penguin)": "penguin", "乌龟 (turtle)": "turtle",
            "蜗牛 (snail)": "snail", "幽灵 (ghost)": "ghost", "蝾螈 (axolotl)": "axolotl",
            "水豚 (capybara)": "capybara", "仙人掌 (cactus)": "cactus", "机器人 (robot)": "robot",
            "兔子 (rabbit)": "rabbit", "蘑菇 (mushroom)": "mushroom", "胖墩 (chonk)": "chonk"
        }
        self.species_map = species_map
        species_combo = ttk.Combobox(filter_frame, textvariable=self.species_var, values=species_list, state="readonly", width=25)
        species_combo.set("任意")
        species_combo.pack(fill=tk.X, pady=(0, 12))

        # 稀有度
        ttk.Label(filter_frame, text="⭐ 稀有度", font=("Helvetica", 9, "bold")).pack(anchor=tk.W, pady=(0, 4))
        self.rarity_var = tk.StringVar(value="any")
        rarity_list = ["任意", "普通 ★ (common)", "不凡 ★★ (uncommon)", "稀有 ★★★ (rare)", "史诗 ★★★★ (epic)", "传说 ★★★★★ (legendary)"]
        rarity_map = {
            "任意": "any", "普通 ★ (common)": "common", "不凡 ★★ (uncommon)": "uncommon",
            "稀有 ★★★ (rare)": "rare", "史诗 ★★★★ (epic)": "epic", "传说 ★★★★★ (legendary)": "legendary"
        }
        self.rarity_map = rarity_map
        rarity_combo = ttk.Combobox(filter_frame, textvariable=self.rarity_var, values=rarity_list, state="readonly", width=25)
        rarity_combo.set("任意")
        rarity_combo.pack(fill=tk.X, pady=(0, 12))

        # 眼睛
        ttk.Label(filter_frame, text="👀 眼睛", font=("Helvetica", 9, "bold")).pack(anchor=tk.W, pady=(0, 4))
        self.eye_var = tk.StringVar(value="any")
        eye_list = ["任意", "小圆点 (·)", "星星眼 (✦)", "叉叉眼 (×)", "大圆眼 (◉)", "蚊香眼 (@)", "空心眼 (°)"]
        eye_map = {
            "任意": "any", "小圆点 (·)": "·", "星星眼 (✦)": "✦", "叉叉眼 (×)": "×",
            "大圆眼 (◉)": "◉", "蚊香眼 (@)": "@", "空心眼 (°)": "°"
        }
        self.eye_map = eye_map
        eye_combo = ttk.Combobox(filter_frame, textvariable=self.eye_var, values=eye_list, state="readonly", width=25)
        eye_combo.set("任意")
        eye_combo.pack(fill=tk.X, pady=(0, 12))

        # 帽子
        ttk.Label(filter_frame, text="🎩 帽子", font=("Helvetica", 9, "bold")).pack(anchor=tk.W, pady=(0, 4))
        self.hat_var = tk.StringVar(value="any")
        hat_list = ["任意", "无 (none)", "皇冠 (crown)", "高顶礼帽 (tophat)", "螺旋桨帽 (propeller)", "光环 (halo)", "法师帽 (wizard)", "冷帽 (beanie)", "小黄鸭 (tinyduck)"]
        hat_map = {
            "任意": "any", "无 (none)": "none", "皇冠 (crown)": "crown", "高顶礼帽 (tophat)": "tophat",
            "螺旋桨帽 (propeller)": "propeller", "光环 (halo)": "halo", "法师帽 (wizard)": "wizard",
            "冷帽 (beanie)": "beanie", "小黄鸭 (tinyduck)": "tinyduck"
        }
        self.hat_map = hat_map
        hat_combo = ttk.Combobox(filter_frame, textvariable=self.hat_var, values=hat_list, state="readonly", width=25)
        hat_combo.set("任意")
        hat_combo.pack(fill=tk.X, pady=(0, 12))

        # 闪光
        ttk.Label(filter_frame, text="✨ 特效", font=("Helvetica", 9, "bold")).pack(anchor=tk.W, pady=(0, 4))
        self.shiny_var = tk.BooleanVar(value=False)
        shiny_check = ttk.Checkbutton(filter_frame, text="仅闪光版本 ✨", variable=self.shiny_var)
        shiny_check.pack(anchor=tk.W, pady=(0, 12))

        # 搜索配置
        ttk.Label(filter_frame, text="⚙️ 搜索配置", font=("Helvetica", 9, "bold")).pack(anchor=tk.W, pady=(12, 4))

        count_frame = ttk.Frame(filter_frame)
        count_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(count_frame, text="返回数量:").pack(side=tk.LEFT)
        self.count_var = tk.IntVar(value=1)
        count_spin = ttk.Spinbox(count_frame, from_=1, to=20, textvariable=self.count_var, width=5)
        count_spin.pack(side=tk.LEFT, padx=(4, 0))

        max_frame = ttk.Frame(filter_frame)
        max_frame.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(max_frame, text="最大尝试:").pack(side=tk.LEFT)
        self.max_var = tk.IntVar(value=5000000)
        max_spin = ttk.Spinbox(max_frame, from_=10000, to=100000000, textvariable=self.max_var, width=10)
        max_spin.pack(side=tk.LEFT, padx=(4, 0))

        # 概率显示
        self.prob_label = ttk.Label(filter_frame, text="📊 概率: 计算中...", foreground="#d97706", wraplength=250)
        self.prob_label.pack(anchor=tk.W, pady=(8, 12))

        # 运行按钮
        button_frame = ttk.Frame(filter_frame)
        button_frame.pack(fill=tk.X, pady=(0, 0))

        self.run_btn = ttk.Button(button_frame, text="🚀 开始搜索", command=self.run_search)
        self.run_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.stop_btn = ttk.Button(button_frame, text="⏹ 停止", command=self.stop_search, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 实时更新概率的回调
        self.species_var.trace('w', lambda *args: self.update_prob_display())
        self.rarity_var.trace('w', lambda *args: self.update_prob_display())
        self.eye_var.trace('w', lambda *args: self.update_prob_display())
        self.hat_var.trace('w', lambda *args: self.update_prob_display())
        self.shiny_var.trace('w', lambda *args: self.update_prob_display())
        self.max_var.trace('w', lambda *args: self.update_prob_display())

    def setup_output(self, parent):
        # 日志
        log_frame = ttk.LabelFrame(parent, text="📋 搜索日志", padding=8)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            width=50,
            font=("Monaco", 9),
            bg="#0d1117",
            fg="#e6edf3",
            insertbackground="#e6edf3"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 结果
        result_frame = ttk.LabelFrame(parent, text="🎯 搜索结果", padding=8)
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=8,
            width=50,
            font=("Monaco", 9),
            bg="#21262d",
            fg="#58a6ff",
            insertbackground="#58a6ff"
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 快速操作
        action_frame = ttk.Frame(result_frame)
        action_frame.pack(fill=tk.X, pady=(8, 0))

        ttk.Button(action_frame, text="📋 复制 UID", command=self.copy_last_uid).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(action_frame, text="📝 打开配置文件", command=self.open_config).pack(side=tk.LEFT)

    def log(self, message, level="info"):
        """添加日志"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def add_result(self, result_dict):
        """添加结果"""
        text = f"""
🎯 [{result_dict['rarity'].upper()}] {result_dict['species']}
   Eye: {result_dict['eye']} | Hat: {result_dict['hat']}
   {'✨ SHINY' if result_dict.get('shiny') else ''}
   UID: {result_dict['uid']}
"""
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.root.update()

    def run_search(self):
        """开始搜索"""
        if not self.buddy_script.exists():
            messagebox.showerror("错误", f"找不到脚本: {self.buddy_script}")
            return

        self.running = True
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)

        # 显示搜索条件
        prob_str = self.estimate_probability()
        self.log(f"📊 {prob_str}\n")

        # 在新线程中运行以不阻塞 UI
        thread = threading.Thread(target=self._search_thread, daemon=True)
        thread.start()

    def update_prob_display(self):
        """实时更新概率显示"""
        prob_str = self.estimate_probability()
        self.prob_label.config(text=prob_str)

    def estimate_probability(self):
        """估算搜索条件的概率"""
        rarity_probs = {
            "any": 1.0,
            "common": 0.60,
            "uncommon": 0.25,
            "rare": 0.10,
            "epic": 0.04,
            "legendary": 0.01
        }

        species_val = self.species_map.get(self.species_var.get(), "any")
        species_prob = 1.0 / 18 if species_val != "any" else 1.0

        rarity_val = self.rarity_map.get(self.rarity_var.get(), "any")
        rarity_prob = rarity_probs.get(rarity_val, 1.0)

        eye_val = self.eye_map.get(self.eye_var.get(), "any")
        eye_prob = 1.0 / 6 if eye_val != "any" else 1.0

        hat_val = self.hat_map.get(self.hat_var.get(), "any")
        hat_prob = (1.0 / 8) if (hat_val != "any" and hat_val != "none") else 1.0

        shiny_prob = 0.01 if self.shiny_var.get() else 1.0

        total_prob = species_prob * rarity_prob * eye_prob * hat_prob * shiny_prob

        # 计算需要的迭代次数
        max_iter = self.max_var.get()
        expected_finds = max(1, int(max_iter * total_prob))

        if total_prob < 0.0001:
            level = "⚠️ 极低"
            advice = "放宽条件"
        elif total_prob < 0.001:
            level = "🔶 较低"
            advice = "增加搜索次数"
        elif total_prob < 0.01:
            level = "🟡 中等"
            advice = "应该能找到"
        else:
            level = "🟢 较高"
            advice = "容易找到"

        return f"{level} 1/{max(1, int(1/total_prob))} | 预期 {expected_finds} 个 | {advice}"

    def _search_thread(self):
        """搜索线程"""
        try:
            # 构建命令
            cmd = ['bun', str(self.buddy_script)]

            species_val = self.species_map.get(self.species_var.get(), "any")
            if species_val != "any":
                cmd.extend(['--species', species_val])

            rarity_val = self.rarity_map.get(self.rarity_var.get(), "any")
            if rarity_val != "any":
                cmd.extend(['--rarity', rarity_val])

            eye_val = self.eye_map.get(self.eye_var.get(), "any")
            if eye_val != "any":
                cmd.extend(['--eye', eye_val])

            hat_val = self.hat_map.get(self.hat_var.get(), "any")
            if hat_val != "any":
                cmd.extend(['--hat', hat_val])

            if self.shiny_var.get():
                cmd.append('--shiny')

            cmd.extend(['--count', str(self.count_var.get())])
            cmd.extend(['--max', str(self.max_var.get())])

            self.log(f"🔍 开始搜索...\n")

            # 运行进程
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # 读取输出
            for line in self.current_process.stdout:
                if not self.running:
                    self.current_process.terminate()
                    break

                line = line.rstrip()
                if line:
                    self.log(line)

                    # 解析结果（简单的启发式方法）
                    if line.startswith('#'):
                        # 这是结果开始，下面会跟上 uid
                        pass

            self.current_process.wait()

            if self.running:
                self.log("\n✅ 搜索完成")

        except Exception as e:
            self.log(f"❌ 错误: {e}")
        finally:
            self.running = False
            self.run_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.current_process = None

    def stop_search(self):
        """停止搜索"""
        self.running = False
        if self.current_process:
            self.current_process.terminate()
        self.log("\n⏹ 已停止搜索")
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def copy_last_uid(self):
        """复制最后一个 UID"""
        result_text = self.result_text.get(1.0, tk.END)
        lines = result_text.strip().split('\n')

        for line in reversed(lines):
            if 'uid' in line.lower() and ':' in line:
                uid = line.split(':')[1].strip()
                if len(uid) == 64 and all(c in '0123456789abcdef' for c in uid):
                    self.root.clipboard_clear()
                    self.root.clipboard_append(uid)
                    messagebox.showinfo("✅ 复制成功", f"已复制到剪贴板")
                    return

        messagebox.showwarning("⚠️ 提示", "没有找到有效的 UID")

    def open_config(self):
        """打开 ~/.claude.json"""
        config_path = Path.home() / '.claude.json'

        if config_path.exists():
            import subprocess
            subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', str(config_path)])
            messagebox.showinfo("📝 使用说明", f"已打开配置文件\n\n"
                              "请在最上面（{开头之后）添加：\n\n"
                              '"userID": "你复制的 UID",\n\n'
                              "然后保存，重启 Claude Code 即可")
        else:
            messagebox.showerror("❌ 错误", f"找不到配置文件\n{config_path}\n\n请先启动 Claude Code 一次")

if __name__ == '__main__':
    root = tk.Tk()
    app = BuddyFinderGUI(root)
    root.mainloop()
