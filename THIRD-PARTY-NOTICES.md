# 第三方来源与许可

本仓库包含两类内容：**本项目自己写的**方法与模板，以及**研读他人资料后提炼的**方法与从别处转载的提示词原文。
下表登记来源、已读范围、许可状态与用途。核对日期为 2026-10-12 至 2026-11-20。

## 一、方法与结构来源

| 来源 | 链接 | 已读范围 | 许可状态 | 本项目如何用 |
| --- | --- | --- | --- | --- |
| ZeroLu / awesome-seedance-2.5 | https://github.com/ZeroLu/awesome-seedance-2.5 | 21 条完整提示词 | 页面未见 LICENSE，按"保留所有权利"理解 | 方法摘要；全文随技能收录，作写稿锚点（见第二节） |
| LearnPrompt / awesome-seedance | https://github.com/LearnPrompt/awesome-seedance | 831 条记录、27 个模板的结构块／指导／陷阱 | 代码 MIT；策展内容 CC BY 4.0；prompt 与媒体归原作者 | 方法摘要 + 结构规则改写（`references/external-library/structural-rules.md`）；45 条全文作锚点 |
| jijiutong / ai-visual-director | https://github.com/jijiutong/ai-visual-director | 导演、镜头预算、运动、表演、提示词组装相关文件与 2 条文字示例 | 未逐项核对，仅作方法研读 | 改写为[导演设计](skills/video-prompt-director/references/directing.md)的一部分 |
| 62656456 / ai-storyboard-director-v5.2 | https://github.com/62656456/ai-storyboard-director-v5.2 | 精编版决策＋全量版部分内容 | 未逐项核对，仅作方法研读 | 同上 |
| liyue-aigc / seedance-2-5-fight-director | https://github.com/liyue-aigc/seedance-2-5-fight-director | 12 个参考文件（约 185 KB）全量阅读 | **无 LICENSE 文件** | 只吸收方法、不复制原文，改写为动作与机位两册 |
| Arvin《AI 打斗的关键一击：冲击帧与闪帧提示词实战》 | https://vibeshot.club/courses/db35b227-98ee-4992-8bce-5eeb0fff2291/learn?lesson=2a58bddc-1285-4ecd-b154-8cc0cac4c70e | 阅读全文，未播放示范视频 | 课程内容，无转载授权 | 只提炼写法，改写为[动作视觉重音](skills/video-prompt-director/references/impact-frames.md) |
| 《电影级 AI 舞蹈视频编舞导演》 | 文稿由使用者提供，归档在 `archive/sources/` | 27 节原文 | 使用者提供，未确认可再分发 | 改写为舞蹈三册；原稿不随技能分发 |

## 二、转载的提示词原文

66 条提示词全文与 852 条目录在 `references/external-library/`，仅作写稿时的锚点。

- 文本著作权属各条原作者；两个来源仓库都只做转载与溯源，不主张这些文本的版权。
- LearnPrompt 一侧：策展内容 CC BY 4.0，prompt 归原作者（本项目未保留逐条作者信息）。
- ZeroLu 一侧：仓库无 LICENSE，按"保留所有权利"理解。
- 自用与朋友间共享，可以整段读、可以改写；不要整段搬进交付给别人的稿子里。
- 将来若要公开发布，先摘掉 `samples-*.md` 与 `catalog.md`，其余功能不受影响。

## 三、平台规格来源

平台规格与提示词语法（[平台口径](skills/video-prompt-director/references/platform-notes.md)）的核对来源与证据等级如下。
未读到的内容不列为已核对；单一来源的条目保持【二手待核】。

| 来源 | 链接 | 核对情况 | 用于 |
| --- | --- | --- | --- |
| Dreamina 官方 Seedance 2.5 提示词指南 | https://dreamina.capcut.com/seedance/seedance-2-5-prompt | 2026-10-12 直接读取正文 | 八段式结构与顺序、`@Image1` 写法、`Preserve`／`Avoid`、负向约束要求、时间戳格式 |
| 字节 Seed 官方 Seedance 2.5 发布说明 | https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5 | 页面为脚本渲染，正文未取到 | 未读到内容，不列为已核对 |
| BytePlus ModelArk 官方提示词指南 | https://docs.byteplus.com/pt/docs/ModelArk/2607689 | 通过检索片段读到部分正文 | 时间戳的三种控制方式、负向控制、首尾帧锁画幅 |
| 多份对同一官方指南的独立转述 | — | 四至五份互相一致，未直接读到原文 | 素材上限与推荐区间、四种声音分隔符、"不得用分别是句式"、"一镜一个主运镜" |

## 四、本项目自有内容

`skills/video-prompt-director/` 下的 SKILL、references、assets、scripts 为自用撰写，未附许可证；
自用与朋友间共享即可，暂不考虑公开发布。
