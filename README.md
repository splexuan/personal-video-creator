# 个人视频创作指南

用于把主题、角色或产品参考、音频和已有脚本写成细致的即梦 / Seedance 中文视频提示词，并根据实际成片反馈积累个人方法。生活情景是其中一种内容类型；目前覆盖 18 类内容，提供 19 份视频参考模板（含单人舞短版）、一份舞蹈参考图提示词起点和 5 组可组合的画风、制作方法。

技能调用名：`$personal-video-creator`。

## 能做什么

- 按内容目标选择模板，设计不同的故事、展示、表演或交互流程。
- 先确定观看终点和具体视觉主意，设计信息显露、调度、表演、切镜与跨镜状态。
- 根据角色多角度参考绑定身份，也支持动物、产品、场景、音频与界面素材。
- 写清表情、动作、接触、材料变化和状态反馈，使画面有具体依据。
- 按类型安排摄影、声音、时长与镜头，生成可以直接复制使用的完整提示词。
- 舞蹈创作按有无参考图引导准备素材，按动作选择半身、七分身或全身，安排动作密度、重音、留白与衔接；素材足够时直接写稿。
- 评价成片并保留实际最终提示词，区分用户认可、直接观察与待确认信息。

提示词结构按内容目标、素材和实际生成入口选择。分类模板提供可调整的参考写法，允许增删、合并、改名与重排；短片也可以用清楚的连续描述或时间线。模块数量不作为质量标准。

产品片使用产品、展示与镜头字段；舞蹈突出音乐、编舞和同步；界面突出布局、交互和状态。生活情景的七模块仍可按需要使用，空栏目和无关要求应删除。选择方法见[共用写法](skills/personal-video-creator/references/video-core.md)。

## 支持的视频类型

当前覆盖以下 **18 类内容**，支持对应的创意设计、分镜、中文视频提示词与成片复盘。共有 **19 份视频参考模板**：音乐 MV 与舞蹈提供 MV 和单人舞两种起点，其余各有一份。每类根据目标选择表演、摄影、声音和时间安排，结构、镜头数、时长与画幅均可调整。

### 故事与记录：5 类

| 视频类型 | 适合创作的内容 | 创作重点 | 模板入口 |
| --- | --- | --- | --- |
| **1. 生活情景** | 家庭日常、情侣或朋友互动、室友小事件、换装互动、日常误会 | 人物关系与事件触发清楚，表情从一个状态自然变化到另一个状态；视线、手部、道具与日常动作连续，结尾完成当前事件 | [生活情景模板](skills/personal-video-creator/assets/life-scene-prompt-template.txt)、[创作方法](skills/personal-video-creator/references/life-scenes.md) |
| **2. 剧情与情感** | 暗恋、告别、重逢、选择、关系变化，以及对白戏或无声表演 | 用对视、停顿、动作中断与回应表现心理变化；给观众理解和人物反应留时间，安排情绪转折与最后的余情 | [剧情模板](skills/personal-video-creator/assets/templates/drama.txt) |
| **3. 反转与荒诞喜剧** | 误会、甩锅、视觉揭晓、重复失败、冷面反应、不合常理的小事件 | 决定观众与角色分别何时知道什么；铺垫、反转与反应有可见依据，笑点落在具体画面、动作或声音上 | [喜剧模板](skills/personal-video-creator/assets/templates/comedy.txt) |
| **4. 动物与萌宠** | 猫狗互动、多宠物小故事、动物陪伴、萌宠日常与宠物喜剧 | 明确每只动物的注意力目标，写动作准备、接触与后续反应；保持数量、体型、位置和行为因果，使互动容易看懂 | [萌宠模板](skills/personal-video-creator/assets/templates/pets.txt) |
| **5. 旅行与日常 Vlog** | 旅行自拍、朋友跟拍、城市漫步、出游记录、日常活动片段 | 明确谁持机、谁出镜，安排可通行路线、自然观察与互动；摄影变化由注意力或行动引起，保留环境声与记录感 | [Vlog 模板](skills/personal-video-creator/assets/templates/vlog.txt) |

### 展示与表演：4 类

| 视频类型 | 适合创作的内容 | 创作重点 | 模板入口 |
| --- | --- | --- | --- |
| **6. 产品与品牌广告** | 产品主视觉、香水或数码产品展示、材料质感、使用演示、品牌短片 | 产品外观与结构稳定，卖点有可见演示；用光线、材料、局部动作与镜头突出重点，安排最后的产品或品牌画面 | [广告模板](skills/personal-video-creator/assets/templates/product-commercial.txt) |
| **7. 人物分享与 UGC 测评** | 面对镜头分享、开箱、实际使用、功能演示、体验与评价 | 口播像自然聊天，人物操作产生可见结果，先观察再回应；人脸与操作画面合理分配，功能、评价和数据依据已提供信息 | [UGC 模板](skills/personal-video-creator/assets/templates/ugc-review.txt) |
| **8. 时装与造型展示** | Lookbook、街拍、走秀、换装、单套或多套穿搭、主题与 Cosplay 造型展示 | 看清整体廓形、材质与鞋包饰品，走步或转身带出衣料动态；同一人物跨造型保持身份，每套服装与换装位置明确 | [时装模板](skills/personal-video-creator/assets/templates/fashion.txt) |
| **9. 音乐 MV 与舞蹈** | 音乐 MV、演唱、舞台表演、美女热舞、单人互动舞、手势舞、服装动态舞与多人编舞 | 判断参考图是否够用，按动作选半身、七分身或全身；设计乐句、动作短句、重音、留白、重心与衔接，表情、衣发和摄影共同服务表演 | [MV 模板](skills/personal-video-creator/assets/templates/music-video.txt)、[单人舞短版](skills/personal-video-creator/assets/templates/dance-short.txt) |

舞蹈按任务继续细分：短随拍与镜头互动侧重连贯律动、手势、眼神和笑容；衣料动态舞侧重身体带动袖口、裙摆与发丝；编舞主导的 MV 或多人舞按实际音乐组织段落、队形与摄影；纯演唱或视觉 MV 只采用需要的表演方法。素材未定时先用[舞蹈创作准备](skills/personal-video-creator/references/dance-preparation.md)，动作与节奏设计使用[统一舞蹈导演](skills/personal-video-creator/references/dance-performance.md)。

### 动作与奇观：5 类

| 视频类型 | 适合创作的内容 | 创作重点 | 模板入口 |
| --- | --- | --- | --- |
| **10. 动作与搏斗** | 攻防、对峙、追逐、闪避、近身搏斗与战斗片段 | 写清行动意图、准备、攻击或移动路径、接触、后果与回位；重心和空间关系可信，摄影能看见关键动作与结果 | [动作模板](skills/personal-video-creator/assets/templates/action.txt) |
| **11. 运动与极限挑战** | 跑跳、球类表现、运动技巧、闯关、跳跃与极限挑战片段 | 路线、起步、承重、腾空或关键动作、落地与完成条件明确；镜头保留重要接地过程，完成后有成绩反馈或人物反应 | [运动模板](skills/personal-video-creator/assets/templates/sports.txt) |
| **12. 车辆与驾驶** | 汽车或摩托展示、驾驶片段、自行车骑行、道路行驶与旅程 | 车辆外形、车轮与接地连续，道路和行进方向清楚；区分车内、车外及跟拍机位，摄影运动与车辆路线相容 | [车辆模板](skills/personal-video-creator/assets/templates/vehicles.txt) |
| **13. 奇幻与科幻** | 异能、魔法、未来科技、异世界、异常变换与视觉奇观 | 先定义能力或异常的规则、作用对象与范围，再写启动、过程、环境反馈和后果；效果发生后保留相应状态 | [奇幻科幻模板](skills/personal-video-creator/assets/templates/fantasy-scifi.txt) |
| **14. 悬疑与恐怖** | 异常征兆、重复空间、被跟随、逐渐逼近、惊悚揭晓与悬念片段 | 控制观众可见的信息，安排异常出现、升级与角色察觉；视线、空间、环境声与最后揭晓相互配合，恐惧有具体来源 | [悬疑恐怖模板](skills/personal-video-creator/assets/templates/horror-suspense.txt) |

### 过程与交互：4 类

| 视频类型 | 适合创作的内容 | 创作重点 | 模板入口 |
| --- | --- | --- | --- |
| **15. 美食与 ASMR** | 烹饪、食物特写、品尝、切剥搅拌、材料触感与近距离声音 | 材料状态随操作改变，动作特写与实际声源对应；安排质感、过程和最后食物状态，品尝时先体验再反应 | [美食 ASMR 模板](skills/personal-video-creator/assets/templates/food-asmr.txt) |
| **16. 制作与改造过程** | 手工、物件制作、整理、空间改造、材料加工与前后对比 | 保留对象和空间基准，按阶段展示可见变化；材料、工具与完成状态接续，延时或蒙太奇说明省略的过程 | [制作改造模板](skills/personal-video-creator/assets/templates/process-transformation.txt) |
| **17. 游戏感任务与直播片段** | 第一或第三人称游戏任务、探索、收集物品、NPC 互动、直播式展示与主播画中画 | 目标、路线、操作和完成条件明确；物品、任务进度与 HUD 随交互变化，游戏机位和主播画面各有归属 | [游戏任务模板](skills/personal-video-creator/assets/templates/gameplay.txt) |
| **18. 界面动效与角色选择** | 页面滚动、按钮与卡片响应、产品界面演示、角色选择、模型展示与局部动效 | 固定布局和准确文案，写清悬停、点击或滚动触发什么响应；选中项、模型与页面状态对应，最后停在明确界面状态 | [界面动效模板](skills/personal-video-creator/assets/templates/interface-motion.txt) |

## 可组合的画风与制作方法

以下 **5 组补充方法**可叠加到上述内容类型，按本片需要选择。动画、复古质感、第一人称和时间特效可以与不同题材组合；分镜驱动用于已有图板或需要分段衔接的制作方式。

| 补充方法 | 支持的表现方式 | 设计重点 | 入口 |
| --- | --- | --- | --- |
| **动画与混合画风** | 2D 动画、3D 动画、定格、贴纸或纸片运动、真人与动画混合 | 明确各层画风、比例、材质与光影，指定连续运动或分步运动，以及允许夸张形变的主体 | [动画补充](skills/personal-video-creator/assets/modifiers/animation.txt) |
| **复古 DV 与档案影像** | 家庭录像、DV 随拍、胶片记录、指定年代的档案影像质感 | 统一年代、介质、服装和物件，画质与录音质感符合记录方式，摄影保留可辨认事件 | [复古影像补充](skills/personal-video-creator/assets/modifiers/retro-footage.txt) |
| **第一人称与连续长镜头** | POV、自拍、目击者记录、动作相机、跟随拍摄、一镜到底或局部连续段 | 明确视角主人与持机条件，设计真实可通行路线、手部占用与注意力变化，保持连续段的时间和空间 | [连续镜头补充](skills/personal-video-creator/assets/modifiers/continuous-take.txt) |
| **时间冻结、倒放与变速** | 世界冻结、局部冻结、倒放、慢动作和指定阶段变速 | 明确作用对象、起止时点、例外主体和声音处理，恢复或倒回后沿用正确状态 | [时间特效补充](skills/personal-video-creator/assets/modifiers/time-effects.txt) |
| **分镜图驱动与分段衔接** | 分镜图转视频、首尾图控制、多个片段接续与后期拼接 | 分配身份图、分镜图与首尾图职责，重建每格完整画面，写清前段末态、后段起态与实际衔接方式 | [分镜驱动补充](skills/personal-video-creator/assets/modifiers/storyboard-driven.txt) |

组合时先确定主要内容目标，再加入需要的表现方法。例如：宠物喜剧＋3D 动画、产品广告＋定格、旅行 Vlog＋复古 DV、追逐片段＋第一人称长镜头、奇幻短片＋时间冻结。混合内容也可以互相借用方法，如车辆广告以产品展示为主，补充道路、车辆和驾驶连续性。

选择与分类依据见[类型与模板索引](skills/personal-video-creator/references/video-types.md)。这些支持范围用于选择创作方法；模板改编的新视频效果根据实际生成结果与用户反馈继续积累。

## 舞蹈导演文档

此前提供的《电影级 AI 舞蹈视频编舞导演》完整原文已加入仓库，保留其 **27 节内容与核心理念**，可以直接点击查看。

| 文档 | 内容与用途 |
| --- | --- |
| [电影级 AI 舞蹈视频编舞导演 · 原文](docs/dance-choreography-director.md) | 完整查看角色与参考图、动作语言、身体力学、音乐乐句、动作衔接、动态对比、表情、衣发、摄影、匹配剪辑、结尾，以及原文的 I2VA / H3 转译与检查要求 |
| [个人指南 · 舞蹈导演整合版](skills/personal-video-creator/references/dance-performance.md) | 适用于本指南的日常舞蹈创作，将导演方法与互动表演、动作密度、重音、停顿和节奏变化结合，再选择短舞或 MV 写法 |
| [个人指南 · 舞蹈创作准备](skills/personal-video-creator/references/dance-preparation.md) | 判断有无参考图及是否需要补图，选择半身、七分身或全身，准备角色图或视频首帧，并引导继续编舞和视频提示词 |

原文按附件原样保存，作为可阅读的导演资料。当前创作采用个人指南的整合方法，动作数量、表情、段落和格式按本次目标及实际生成入口选择。

## 结构

`docs/` 保存导演原文；可安装的个人技能位于以下目录。

```text
skills/personal-video-creator/
├── SKILL.md                         技能入口和工作流程
├── agents/openai.yaml               显示名称与调用提示
├── assets/
│   ├── life-scene-prompt-template.txt 生活情景参考写法
│   ├── dance-reference-image-template.txt 舞蹈角色图或首帧提示词起点
│   ├── templates/                  其他内容模板及单人舞短版
│   └── modifiers/                  5 组画风与制作方法补充写法
└── references/
    ├── preferences.md               个人偏好及适用范围
    ├── video-types.md               类型选择、模板与方法入口
    ├── video-core.md                多类型共用写法与检查标准
    ├── directing.md                 观看目标、视觉主意与镜头决策
    ├── life-scenes.md               生活情景创作方法
    ├── dance-preparation.md         参考图分支、取景选择与创作推进
    ├── dance-performance.md         舞蹈导演：节奏、编舞、力学、表情与摄影
    ├── feedback.md                  成片反馈与维护方法
    ├── external-methods.md          外部方法、来源与适用条件
    ├── external-cases.md            提示词研读提炼的方法
    ├── case-index.md                案例状态与资料索引
    └── cases/                       个人案例说明及已有提示词
```

从[技能入口](skills/personal-video-creator/SKILL.md)阅读。新创作或重做镜头方案先使用[导演设计](skills/personal-video-creator/references/directing.md)，再结合[共用写法](skills/personal-video-creator/references/video-core.md)和本次对应的模板；小范围修改保留已有设计。参考自己以前的作品时查看[个人案例索引](skills/personal-video-creator/references/case-index.md)。

## 外部方法参考

已从 ZeroLu 的社区案例库及 LearnPrompt 的案例与方法库整理参考，主要用于素材分工、喜剧笑点时间安排和逐镜复盘。详见[来源与适用条件](skills/personal-video-creator/references/external-methods.md)，仅保留必要的文字方法来源，不写入外部网址。

已逐条研读 ZeroLu 的 21 条完整记录，并从 LearnPrompt 的 795 条记录中累计选读 47 条，覆盖其快照的 27 种分类。47 条中含两条分镜页生图稿，已与视频提示词区分；本次没有逐条播放或重新生成外部视频。

生活情景的连续情绪、构图揭晓、道具因果和日常收尾见[提示词研读方法](skills/personal-video-creator/references/external-cases.md)。其他类型的模板与分类对应见[类型索引](skills/personal-video-creator/references/video-types.md)。模板保留具体方法，外部样片仅供分析，不收录样片资料或网址。

外部已有验证的案例可直接按题材参考；新故事的生成结果继续单独积累。含蓄情感戏的无声停顿、猫狗双角色等当前剧情要求优先；某个外部案例的特定限制不作为通用要求。

已将 AI Visual Director 的素材分工、调度、视线、表演与状态方法，以及 AI Storyboard Director v5.2 的观看终点、视觉概念、信息显露与镜头衔接方法，落实到技能流程、[导演设计](skills/personal-video-creator/references/directing.md)和相关模板。研读范围、适配与未采用的源项目规则见该文件的来源说明。直接交付可用提示词，结构按类型选择；不要求先安装源项目或补做整套参考图。

用户此前提供的[《电影级 AI 舞蹈视频编舞导演》原文](docs/dance-choreography-director.md)与参考分析提炼的互动表演方法已整合到[统一舞蹈导演](skills/personal-video-creator/references/dance-performance.md)：共同设计音乐乐句、动作短句、身体力学、过渡动量、动态对比、表情、衣发与摄影，再按短互动舞或 MV 的目标选择提示词结构。原文中的固定动作数、旋转次数、表情禁用及 H3 / I2VA 专用格式不作为所有舞蹈的默认限制。

舞蹈的[创作准备](skills/personal-video-creator/references/dance-preparation.md)区分已有合用图、局部图与无图：需要复用身份、完整造型或首帧时建议准备图片，一次性文字创作可以直接写视频稿。半身侧重表情与上半身，七分身兼顾肩髋膝，全身看关键步法与地面；参考图景别与视频景别分别选择。需要准备图时交付[参考图提示词](skills/personal-video-creator/assets/dance-reference-image-template.txt)，用户已授权生成才执行生图，随后检查并继续编舞。

编舞节奏区分音乐脉冲、动作速度、动作密度和能量，设计重音、延长、短停、回收与变奏。已有音频按实际听审安排，无音频先给可调整的节奏设计；不把快音乐等同于大量动作，也不把八拍当固定秒数。MV 时间线按实际段落展开，不预设五段结构。

## 安装

本仓库包含一个技能，目录为 `skills/personal-video-creator`。下载或克隆仓库后，把该目录整体放到个人 Codex 技能目录中；设置了 `CODEX_HOME` 时使用其 `skills` 子目录，否则使用用户主目录下的 `.codex/skills`。

最终目录应是 `skills/personal-video-creator/SKILL.md`，不要把仓库的外层目录一起套进去。

当前创建者的电脑已安装该技能；这里保存可追踪的仓库版本。已有安装需要更新时，先保留本机新增的案例和偏好，再同步所需版本。

## 使用示例

> 用 $personal-video-creator，按这两张角色参考图，写一条十秒的生活情景喜剧。两人在家抢遥控器，反转要自然，表情写细，输出完整提示词。

> 用 $personal-video-creator，按这张香水产品图，写一条十二秒的产品广告。突出瓶身和喷雾质感，纯产品展示，输出完整提示词。

> 用 $personal-video-creator，按这张角色图和上传的音频片段，写一条舞蹈 MV。先依据实际音频分配表演段落，再细化动作与摄影。

> 用 $personal-video-creator，按这张成年角色图写一条单人互动舞。固定机位，动作连贯，眼神和笑容自然，服装随动作响应；音乐尚未提供时先写可调整的表演段落。

> 用 $personal-video-creator，我还没有角色图，想做一条轻松互动舞。先推荐适合的角色造型、半身/七分身/全身取景，并给参考图提示词和下一步编舞方向。

短随拍和手势舞使用[单人舞短版](skills/personal-video-creator/assets/templates/dance-short.txt)，音乐表演可用 MV 模板；两者都依据[统一舞蹈导演](skills/personal-video-creator/references/dance-performance.md)，无需填满五个段落或增加无关剧情。

也可要求“给几个机制不同的创意”“按个人视频指南修改节奏”，或提供实际成片和最终提示词进行复盘。已有分镜图时可以使用分镜驱动方法；通常创作不要求先制作图板。

中文、即梦 / Seedance 是当前常用偏好。9:16、电影感写实常用于生活情景，其他类型按内容选择画幅和风格。本次用户要求可以覆盖；第一人称、时长、镜头数、音乐和结尾不固定。

## 已收录案例

| 案例 | 状态 |
| --- | --- |
| 女仆装攻防战 | 用户认可情绪与表情；保存方法摘要，未标为逐字最终稿或直接看片结论 |
| 明天 | 用户整体正面反馈；保留最终提示词，已核对关键画面并记录连续反应与结尾动作；声音未完成听审 |
| 狗打的 | 待用户确认；保留现存十秒稿和画面复盘，实际提交稿对应关系未确认 |

## 持续维护

满意成片用于学习时，保留实际使用的最终提示词原文，并记录认可的是总体效果还是具体细节。案例经验先放案例说明，明确长期偏好进入偏好文件，可推广的方法进入创作方法文件。

本机已安装技能的后续修改需要同步到本仓库后再提交。新类别有实际请求和具体案例方法时再扩展；外部案例支持的模板与个人成片已验证的方法分开记录。

本仓库提交创作方法、模板与个人最终提示词；外部样片仅供参考分析，不写入样片资料、账号、视频文件名、视频地址或网址。
