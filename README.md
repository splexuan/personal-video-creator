# 个人视频创作指南

用于把生活情景、角色参考图和已有脚本写成细致的即梦 / Seedance 中文视频提示词，并根据实际成片反馈积累个人方法。当前成熟模块为生活情景短片，其他类别按实际创作需求逐步扩展。

技能调用名：`$personal-video-creator`。

## 能做什么

- 设计机制不同的生活情景创意，避免只替换人物、服装和台词。
- 根据角色多角度参考绑定身份，写清服装、空间关系、摄影、声音和动作连续性。
- 用可见的视线、表情、呼吸、身体动作和停顿表达情绪。
- 按故事安排时长与镜头，生成可以直接复制使用的完整提示词。
- 评价成片并保留实际最终提示词，区分用户认可、直接观察与待确认信息。

完整提示词使用七个模块：

【角色绑定】【服装】【视角与摄影】【场景】【声音】【镜头】【执行要求】

## 结构

```text
skills/personal-video-creator/
├── SKILL.md                         技能入口和工作流程
├── agents/openai.yaml               显示名称与调用提示
├── assets/
│   └── life-scene-prompt-template.txt 七模块空白模板
└── references/
    ├── preferences.md               个人偏好及适用范围
    ├── life-scenes.md               生活情景创作方法
    ├── feedback.md                  成片反馈与维护方法
    ├── external-methods.md          外部方法、来源与适用条件
    ├── case-index.md                案例状态与资料索引
    └── cases/                       案例说明及已有提示词
```

从[技能入口](skills/personal-video-creator/SKILL.md)阅读，或直接查看[提示词模板](skills/personal-video-creator/assets/life-scene-prompt-template.txt)与[案例索引](skills/personal-video-creator/references/case-index.md)。

## 外部方法参考

已从 [ZeroLu 的社区案例库](https://github.com/ZeroLu/awesome-seedance-2.5)及 [LearnPrompt 的分类方法库](https://github.com/LearnPrompt/awesome-seedance)整理可选参考，主要用于素材分工、喜剧笑点时间安排和逐镜复盘。详见[来源与适用条件](skills/personal-video-creator/references/external-methods.md)，链接保留本次核对的源版本。

这些方法的个人迁移效果仍待成片验证。含蓄情感戏的无声停顿、猫狗双角色等当前剧情要求继续优先；不把某个外部模板的特定限制当作通用要求。

## 安装

本仓库包含一个技能，目录为 `skills/personal-video-creator`。下载或克隆仓库后，把该目录整体放到个人 Codex 技能目录中；设置了 `CODEX_HOME` 时使用其 `skills` 子目录，否则使用用户主目录下的 `.codex/skills`。

最终目录应是 `skills/personal-video-creator/SKILL.md`，不要把仓库的外层目录一起套进去。

当前创建者的电脑已安装该技能；这里保存可追踪的仓库版本。已有安装需要更新时，先保留本机新增的案例和偏好，再同步所需版本。

## 使用示例

> 用 $personal-video-creator，按这两张角色参考图，写一条十秒的生活情景喜剧。两人在家抢遥控器，反转要自然，表情写细，输出完整提示词。

也可要求“给几个机制不同的生活情景创意”“按个人视频指南修改节奏”，或提供实际成片和最终提示词进行复盘。

中文、即梦 / Seedance、9:16、电影感写实是当前常用偏好。本次用户要求可以覆盖；第一人称、时长、镜头数、音乐和结尾不固定。

## 已收录案例

| 案例 | 状态 |
| --- | --- |
| 女仆装攻防战 | 用户认可情绪与表情；保存方法摘要，未标为逐字最终稿或直接看片结论 |
| 明天 | 用户整体正面反馈；保留最终提示词，已核对关键画面并记录连续反应与结尾动作；声音未完成听审 |
| 狗打的 | 待用户确认；保留现存十秒稿和画面复盘，实际提交稿对应关系未确认 |

## 持续维护

满意成片用于学习时，保留实际使用的最终提示词原文，并记录认可的是总体效果还是具体细节。案例经验先放案例说明，明确长期偏好进入偏好文件，可推广的方法进入创作方法文件。

本机已安装技能的后续修改需要同步到本仓库后再提交。新增类别有实际请求和可复用方法时再增加资料与入口，避免预建空模块。

本仓库提交技能文本和示例提示词，不包含角色原图、生成视频、凭据或临时依赖。
