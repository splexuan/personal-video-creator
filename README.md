# 个人视频创作指南

用于把主题、角色或产品参考、音频、已有脚本和参考视频整理成细致的即梦 / Seedance 等中文视频提示词，并根据实际成片反馈积累个人方法。支持参考视频逆向、换人复用和必要参考图制作。生活情景是其中一种内容类型；目前覆盖 18 类内容，提供 19 份视频参考模板（含单人舞短版）、一份舞蹈参考图提示词起点和 5 组可组合的画风、制作方法。

技能调用名：`$personal-video-creator`。

## 能做什么

- 按内容目标选择模板，设计不同的故事、展示、表演或交互流程。
- 只有一个模糊想法时，先发散出几个机制不同的候选并淘汰择优，不让第一条思路直接成为全片。
- 先确定观看终点和具体视觉主意，设计信息显露、调度、表演、切镜与跨镜状态。
- 根据角色多角度参考绑定身份，也支持动物、产品、场景、音频与界面素材。
- 写清表情、动作、接触、材料变化和状态反馈，使画面有具体依据。
- 按类型安排摄影、声音、时长与镜头，生成可以直接复制使用的完整提示词。
- 把简短想法发展为具体构图、空间、光线、镜头运动和观看过程，结合摄影与画面设计检查整段表达。
- 核实参考视频的时间轴、动作和转场，按需准备人物、造型或首尾帧，优先交付一条完整提示词；换人或改输入模式时同步整稿与参考图。
- 舞蹈由 AI 设计完整表演，安排可记住的主动作、段落发展与对比、节奏、高光和结尾；按有无参考图引导准备素材，按动作选择取景，素材足够时直接写稿。
- 评价成片并保留实际最终提示词，区分用户认可、直接观察与待确认信息。

提示词结构按内容目标、素材和实际生成入口选择。分类模板提供可调整的参考写法，允许增删、合并、改名与重排；短片也可以用清楚的连续描述或时间线。模块数量不作为质量标准。

产品片使用产品、展示与镜头字段；舞蹈突出音乐、编舞和同步；界面突出布局、交互和状态。生活情景的七模块仍可按需要使用，空栏目和无关要求应删除。选择方法见[共用写法](skills/personal-video-creator/references/video-core.md)。

## 参考视频逆向与换人复用

提供具体视频时，先核实实际文件与参数，抽帧定位镜头、连续变化、遮挡转场和片尾，再把可观察的动作、摄影、服装与背景状态整理成完整提示词。参考图按实际需要制作；只上传图片时，正文完整承担动作、镜头和节奏，不继续依赖未上传的视频。详细流程见[视频逆向与复刻](skills/personal-video-creator/references/video-reverse-engineering.md)。

人物替换分别指定身份与服装来源，检查旧发型、旧配饰和参考模式是否在整稿中同步更新。标识、文字和片尾按当前要求保留、替换或删除；多造型图作为同一人物的造型顺序，不作为多人并排视频或拼图首帧。

成片复查不仅确认每套造型出现，还要核对旧衣物与转换材料是否收干净、换装后背景是否延续、后半段动作与结尾是否执行。原片观察、文本推演、参考图检查和新视频验证分别记录；未修复的问题保留待验证状态，不包装成成功案例。

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
| **9. 音乐 MV 与舞蹈** | 音乐 MV、演唱、舞台表演、美女热舞、单人互动舞、手势舞、服装动态舞与多人编舞 | 设计有记忆点、节奏、发展、对比、高光和结束关系的完整表演；按参考图与动作选取景，细化身体、表情、衣发、音乐和摄影 | [MV 模板](skills/personal-video-creator/assets/templates/music-video.txt)、[单人舞短版](skills/personal-video-creator/assets/templates/dance-short.txt) |

舞蹈按任务继续细分：短随拍与镜头互动侧重连贯律动、手势、眼神和笑容；衣料动态舞侧重身体带动袖口、裙摆与发丝；编舞主导的 MV 或多人舞按实际音乐组织段落、队形与摄影；纯演唱或视觉 MV 只采用需要的表演方法。素材未定时先用[舞蹈创作准备](skills/personal-video-creator/references/dance-preparation.md)，动作与节奏设计使用[统一舞蹈导演](skills/personal-video-creator/references/dance-performance.md)。

### 动作与奇观：5 类

| 视频类型 | 适合创作的内容 | 创作重点 | 模板入口 |
| --- | --- | --- | --- |
| **10. 动作与搏斗** | 攻防、对峙、追逐、闪避、近身搏斗与战斗片段 | **先按动作单元定密度（目标落地值的两到三倍），再写画面**：写清行动意图、准备、攻击或移动路径、接触、后果与回位；重心和空间关系可信，摄影能看见关键动作与结果。方法见[动作密度与节奏](skills/personal-video-creator/references/pacing.md)、[动作与受力语法](skills/personal-video-creator/references/action-craft.md)与[机位可行性与冲击预算](skills/personal-video-creator/references/camera-feasibility.md) | [动作模板](skills/personal-video-creator/assets/templates/action.txt) |
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
| [个人指南 · 完整舞蹈编排](skills/personal-video-creator/references/dance-composition.md) | 面向短视频表演展示，由 AI 选择主句、变奏、对比与高光，组织整支舞的节奏和结束关系，检查动作同质与构图冲突 |
| [个人指南 · 舞蹈导演整合版](skills/personal-video-creator/references/dance-performance.md) | 适用于本指南的日常舞蹈创作，将导演方法与互动表演、动作密度、重音、停顿和节奏变化结合，再选择短舞或 MV 写法 |
| [个人指南 · 舞蹈创作准备](skills/personal-video-creator/references/dance-preparation.md) | 判断有无参考图及是否需要补图，选择半身、七分身或全身，准备角色图或视频首帧，并引导继续编舞和视频提示词 |

原文按附件原样保存，作为可阅读的导演资料。当前创作采用个人指南的整合方法，动作数量、表情、段落和格式按本次目标及实际生成入口选择。

完整舞蹈先设计整体观看发展，再写动作短句，最后细化身体与摄影。记忆点有具体路径、节奏和轮廓，段落区别让观众看得见，高光有真实动作变化，结尾回应前段或完成运动。柔美舞也可以有快发慢收、停点和朝向变化；结构随风格、音乐和时长选择，不固定套用一套起承转合，也不靠反复伸展填满较长时长。

## 结构

交付视频提示词前，执行[逐段自检与修正](skills/personal-video-creator/references/prompt-self-check.md)，检查因果、空间、连续性、表演容量与指令冲突。需要冲击帧、闪白、反相或闪黑时，使用[动作视觉重音](skills/personal-video-creator/references/impact-frames.md)，将效果绑定到具体事件，并接续恢复后的动作结果。打斗、追逐、群战或冲撞等对抗片先读[动作密度与节奏](skills/personal-video-creator/references/pacing.md)定动作单元总数与幅度，再读[动作与受力语法](skills/personal-video-creator/references/action-craft.md)与[机位可行性与冲击预算](skills/personal-video-creator/references/camera-feasibility.md)。成片被反馈"像减速、站在原地等时间"时用 `scripts/motion-audit.py` 实测定位死区；被反馈"一直在动但不像打斗"时用 `scripts/fight-metrics.py` 实测幅度与打击声，两者都不要凭感觉改词。确认平台能力、素材上限、引用标签或提示词语法时读[平台口径与已核事实](skills/personal-video-creator/references/platform-notes.md)。这些方法已接入技能入口和相应创作流程；文本检查与成片验证分别记录。

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
├── scripts/                        成片实测脚本：运动能量、幅度与打击声
└── references/
    ├── preferences.md               个人偏好及适用范围
    ├── video-types.md               类型选择、模板与方法入口
    ├── video-core.md                多类型共用写法与检查标准
    ├── video-reverse-engineering.md  视频逆向、参考图准备、换人复用与成片对照
    ├── creative-divergence.md        创意发散、视觉机制与方案淘汰
    ├── directing.md                 观看目标、视觉主意与镜头决策
    ├── cinematography.md            构图、空间、光影、运动、画面强度与整段观看体验
    ├── action-craft.md              七拍动作链、受力四通道与尺度、空间调度、技能生命周期与动作容量
    ├── pacing.md                    动作密度与幅度指标、持物轨迹、节奏型与成片实测判据
    ├── camera-feasibility.md        机位风险与安全替代、遮挡转场、冲击预算、能力框与两条产线
    ├── impact-frames.md             冲击帧、闪白、反相与闪黑的写法
    ├── platform-notes.md            平台规格与提示词语法，逐条标注证据等级
    ├── prompt-self-check.md         交付前的逐段自检与修正
    ├── life-scenes.md               生活情景创作方法
    ├── dance-preparation.md         参考图分支、取景选择与创作推进
    ├── dance-composition.md         整支舞的记忆点、发展、节奏、对比与高光
    ├── dance-performance.md         舞蹈导演：节奏、编舞、力学、表情与摄影
    ├── feedback.md                  成片反馈与维护方法
    ├── external-methods.md          外部方法、来源与适用条件
    ├── external-cases.md            提示词研读提炼的方法
    ├── external-library/            外部提示词库：索引、金牌样本全文与模板结构规则
    ├── case-index.md                案例状态与资料索引
    └── cases/                       个人案例说明及已有提示词
```

技能内另有 `scripts/motion-audit.py`：输入一条成片，输出逐秒运动能量、最长近静止区间、运动最高点落位与帧复制检查，用于客观判断动作类短片"够不够快"。配套的 `scripts/fight-metrics.py` 管第二件事：输出高强度帧占比、爆发帧占比、逐秒峰均比、单帧最大位移与音频峰值，直接对"动得够不够大、打击声有没有打实"给出通过／不足，并可用 `--ref` 与参照片并排对照。判据与用法见[动作密度与节奏](skills/personal-video-creator/references/pacing.md)。

从[技能入口](skills/personal-video-creator/SKILL.md)阅读。新创作或重做镜头方案先使用[导演设计](skills/personal-video-creator/references/directing.md)，再结合[摄影与画面设计](skills/personal-video-creator/references/cinematography.md)、[共用写法](skills/personal-video-creator/references/video-core.md)和本次对应的模板；小范围修改保留已有设计。具体视频反推使用[视频逆向与复刻](skills/personal-video-creator/references/video-reverse-engineering.md)。参考自己以前的作品时查看[个人案例索引](skills/personal-video-creator/references/case-index.md)。

## 外部方法参考

下表汇总已研读并融合的方法来源。只登记实际阅读与采用的范围；具体适用条件见[外部方法参考](skills/personal-video-creator/references/external-methods.md)。

| 参考来源 | 已读范围 | 提炼与融合内容 | 方法入口 |
| --- | --- | --- | --- |
| [ZeroLu / awesome-seedance-2.5](https://github.com/ZeroLu/awesome-seedance-2.5) | 21 条完整提示词，2026-10-12 起全量收录 | 连续情绪与表演、构图揭晓、道具因果、异常规则和日常收尾 | [外部提示词库](skills/personal-video-creator/references/external-library/index.md)、[提示词研读方法](skills/personal-video-creator/references/external-cases.md) |
| [LearnPrompt / awesome-seedance](https://github.com/LearnPrompt/awesome-seedance) | 831 条记录，2026-10-12 起全量收录；另收录其 27 个模板的结构块、指导与陷阱 | 参考素材分工、喜剧笑点时间安排、类型模板与逐镜复盘；模板结构与锚点样本 | [外部提示词库](skills/personal-video-creator/references/external-library/index.md)、[模板结构规则](skills/personal-video-creator/references/external-library/structural-rules.md)、[外部方法](skills/personal-video-creator/references/external-methods.md) |
| [jijiutong / AI Visual Director](https://github.com/jijiutong/ai-visual-director) | 相关引擎、表演指导及 2 条文字示例 | 素材职责、空间调度、视线、表演停顿与跨镜状态 | [导演设计](skills/personal-video-creator/references/directing.md) |
| [62656456 / AI Storyboard Director v5.2](https://github.com/62656456/ai-storyboard-director-v5.2) | 精编版相关决策与全量版部分内容 | 观看终点、视觉主意、信息显露、切镜选择和事件线衔接 | [导演设计](skills/personal-video-creator/references/directing.md) |
| [《电影级 AI 舞蹈视频编舞导演》](docs/dance-choreography-director.md) | 用户提供的完整 27 节原文 | 音乐乐句、动作短句、身体力学、过渡动量、动态对比、表情、衣发与摄影；结合互动表演方法组织短舞和 MV | [原文](docs/dance-choreography-director.md)、[统一舞蹈导演](skills/personal-video-creator/references/dance-performance.md)、[完整编排](skills/personal-video-creator/references/dance-composition.md) |
| [Arvin《AI打斗的关键一击：冲击帧与闪帧提示词实战》](https://vibeshot.club/courses/db35b227-98ee-4992-8bce-5eeb0fff2291/learn?lesson=2a58bddc-1285-4ecd-b154-8cc0cac4c70e) | 2026-10-10 阅读全文，未播放示范视频 | 将冲击帧、闪白、反相和闪黑绑定到具体事件；保留接触信息，明确恢复与动作后果，接入动作模板、自检和成片复盘 | [动作视觉重音](skills/personal-video-creator/references/impact-frames.md)、[动作模板](skills/personal-video-creator/assets/templates/action.txt)、[提示词自检](skills/personal-video-creator/references/prompt-self-check.md) |
| [liyue-aigc / seedance-2-5-fight-director](https://github.com/liyue-aigc/seedance-2-5-fight-director) | 2026-10-12 全量读取其 12 个参考文件（约 185 KB）并改写吸收；**该仓库无 LICENSE 文件，只吸收方法、不复制原文** | 七拍动作链、受力反馈四通道与尺度分级、反馈链目录、空间调度与介质层穿越三段式、能力与武器生命周期六步、环境破坏五级、声音五层、动作容量成本表、群体战密度、群战与对轰规则、机位可行性黑名单、遮挡转场、冲击预算、单段能力框与两条产线 | [动作与受力语法](skills/personal-video-creator/references/action-craft.md)、[机位可行性与冲击预算](skills/personal-video-creator/references/camera-feasibility.md)、[动作模板](skills/personal-video-creator/assets/templates/action.txt) |

文字研读、样片观察和个人生成验证分别记录。上述案例库未逐条播放或重新生成；其他来源也不因方法已接入而视为个人成片验证通过。外部特定的时长、动作数、角色数量或专用格式，按当前目标筛选使用。

后续每次新增或扩展外部参考，同步维护本表与[来源记录](skills/personal-video-creator/references/external-methods.md)：来源名称必须附已核对的原始链接，开源项目链接到对应仓库，教程链接到原课程页；用户提供且无公开来源的文稿链接到仓库内原文，不推测开源地址。同时注明实际已读范围、采用的方法和对应入口；已有来源补充研读时更新原行。不收录外部样片资料或样片网址。

## 平台口径来源

核对 Seedance 2.5 与即梦 / Dreamina 的平台规格与提示词语法时使用的来源。逐条结论与证据等级见[平台口径与已核事实](skills/personal-video-creator/references/platform-notes.md)。

| 来源 | 核对日期与实际读到什么 | 用于 |
| --- | --- | --- |
| [Dreamina 官方 Seedance 2.5 提示词指南](https://dreamina.capcut.com/seedance/seedance-2-5-prompt) | 2026-10-12 **直接读取正文**；页面标注 Aug 18, 2026 | 八段式结构与固定顺序、素材标签写法、`Preserve`／`Avoid` 模板、负向约束的写法要求、时间戳示例格式、"关键指令只说一次" |
| [字节 Seed 官方 Seedance 2.5 发布说明](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) | 2026-10-12 两次尝试，**页面为脚本渲染，正文未取到**；官方模型页同样未取到 | 未读到内容，不列为已核对 |
| [BytePlus ModelArk 官方 Seedance 2.5 提示词指南](https://docs.byteplus.com/pt/docs/ModelArk/2607689) | 2026-10-12 通过公开检索片段读到部分正文；直接打开英文与中文页面均为空页 | 时间戳的三种控制方式与连续性要求、负向控制（字幕／BGM／音频）、首尾帧锁画幅、白模参考 |
| 多份对同一官方指南的独立转述（含一份官方指南的完整中文译本） | 2026-10-12；四至五份来源互相一致，本次**未能直接读到官方原文** | 素材上限与推荐区间、四种声音与文字分隔符、参考素材"不得用'分别是'句式"的规则、"一镜一个主运镜" |

未读到的内容不列为已核对；单一来源的条目在平台口径册中保持【二手待核】，不因登记而升格为平台事实。平台规格会变化，实际入口优先。

## 安装

本仓库包含一个技能，目录为 `skills/personal-video-creator`。下载或克隆仓库后，把该目录整体放到个人 Codex 技能目录中；设置了 `CODEX_HOME` 时使用其 `skills` 子目录，否则使用用户主目录下的 `.codex/skills`。

最终目录应是 `skills/personal-video-creator/SKILL.md`，不要把仓库的外层目录一起套进去。

当前创建者的电脑已安装该技能；这里保存可追踪的仓库版本。已有安装需要更新时，先保留本机新增的案例和偏好，再同步所需版本。

## 使用示例

> 用 $personal-video-creator 反推这个视频，换成我提供的人物，只上传参考图，给我一条完整提示词；标识和片尾按这次要求处理。

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
| 女仆装攻防战 | 用户认可整体效果，此前已认可情绪与表情；保存方法摘要，未标为逐字最终稿或直接看片结论 |
| 明天 | 用户认可整体效果；保留最终提示词，已核对关键画面并记录连续反应与结尾动作；声音未完成听审 |
| 狗打的 | 用户认可整体效果；保留现存十秒稿和画面复盘，实际提交稿对应关系未确认 |
| 地铁复仇喜剧 | 用户认可整体效果（认可对象为经用户后期加工的第一版，文件参数不代表生成规格）；保留提示词原文，已核对画面与文字区域逐帧；收尾字幕多字与同句配音念错已确认为生成端所出 |
| 气球沙发升空（西游记三人组） | 用户认可整体效果；保留参考静帧与视频两份提示词，已核对成片两张抽帧与文件参数（3:4 落地正确、开场按文字走）；人声语感问题为用户反馈，未听审 |
| 樱花庭院古装人像 | 用户认可整体效果；保留提示词原文，本次未查看成片；人体结构与机位的主动约束已提炼进共用写法，未声称已在成片验证 |
| 东方玄幻樱花剑尊特效片 | 用户认可整体效果（提交收录即记认可）；保留提示词原文，本次未查看成片；“无血液以主题材质替代”与动作密度上限已提炼进动作模板，不声称已生成成功 |
| 魔法笔·街道交通 Vlog | 用户认可整体效果（提交收录即记认可）；保留提示词原文，未查看成片；“变形锚定”（换外观、保运动学）已提炼进混合画风补充写法；稿内两处光照规则互斥照旧保留 |
| 真人自拍特写（皮肤质感） | 用户认可整体效果（提交收录即记认可）；保留提示词原文（含原文重复段与混用时间码），未查看成片；真实质感的分级写法已提炼进共用写法，“无磨皮／（磨皮感）”用词冲突照旧标出 |
| 在湖边，把时间忘了 | 未达到目标；用户明确反馈表达不明。保留交付稿与抽帧复盘，用于诊断观看过程和情绪表达不足，实际提交稿未确认，不作成功参考 |
| 香港动作片后巷打斗 | 分层结论：美术层通过、节奏层失败；用户反馈“打斗不流畅、节奏不紧凑、好像减速了一样、站在原地等时间”。已用运动能量实测定位 5.29 秒死区（正好落在写明的决胜段）、最高点落在转场、零重复帧。保留 v1 交付稿与失败复盘，四条根因与量化诊断法已提炼进动作密度方法，不作成功参考 |
| 外卖仔打斗（《滚汤》修正稿 v2.1） | 分层结论：密度层通过、幅度层失败、连续性层失败。上一版整改有效——最长近静止区间由 5.29 秒降到 0.12 秒、全片无死区；用户新反馈“穿帮太多了”“根本没有打斗的感觉”并提交一条参照短片，实测对照为高强度帧占比 7.6%（参照 24.3%）、爆发帧 4.0%（参照 9.3%）、强打击点 0 个（参照 2 个），即“一直在动但都不大”。逐帧确认六处穿帮（锅盖状态矛盾、空锅不空、持物塌回静态摆姿、后段环境物消失、收尾未落地、铁闸与床单不见）。保留 v2.1 交付稿与失败复盘，五条根因与幅度指标已提炼进动作密度与节奏方法，不作成功参考 |

## 持续维护

用户提交稿件要求收录即视为整体认可，不必再追问效果意见。满意成片用于学习时，保留实际使用的最终提示词原文，并记录认可的是总体效果还是具体细节。案例经验先放案例说明，明确长期偏好进入偏好文件，可推广的方法进入创作方法文件。

本机已安装技能的后续修改需要同步到本仓库后再提交。新类别有实际请求和具体案例方法时再扩展；外部案例支持的模板与个人成片已验证的方法分开记录。

新增或扩展外部方法参考时，同次更新上方参考表和技能中的来源记录，核对方法入口、阅读范围与验证状态，再同步安装版本并提交仓库。

本仓库提交创作方法、模板与个人最终提示词；外部样片仅供参考分析，不写入样片资料、账号、视频文件名或样片网址。README 的参考来源保留可点击的原始仓库、教程或文稿链接。
