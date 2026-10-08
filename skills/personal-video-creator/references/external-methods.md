# 外部方法参考

用于多素材分工、反转喜剧和逐镜复盘。案例库的已有验证案例可以作为创作参考；直接研读完整提示词的记录见[案例研读](external-cases.md)。两个导演项目的创作决策已接入[导演设计](directing.md)，在新创作与镜头重写时使用。新故事的生成结果另行记录。日常使用读取本地摘要即可；需要新增案例或确认平台能力时，再检查对应原始资料或官方说明。

## 来源与用途

| 来源 | 当前用途 | 采用范围 |
| --- | --- | --- |
| [ZeroLu / awesome-seedance-2.5](https://github.com/ZeroLu/awesome-seedance-2.5/blob/a24d31c3909a30b97aec83e6b48867c4482cc68e/README-zh.md) | 已研读 21 条完整提示词，研究情绪、摄影、道具和异常规则 | 保留原提示词与来源链；本次未逐条播放或重新生成视频 |
| [LearnPrompt / awesome-seedance](https://github.com/LearnPrompt/awesome-seedance/tree/487c166e2f09487016452b90fec5e19a470af883) | 筛查案例索引，累计研读 47 条提示词记录，并参考分类与复盘流程 | 按[类型索引](video-types.md)选择写法；含两条分镜页生图稿，保留其性质 |
| [jijiutong / AI Visual Director](https://github.com/jijiutong/ai-visual-director/tree/b47f664ca00c50539c5365109e9360f82170972d) | 已接入素材职责、调度、视线、表演停顿和跨镜状态 | 研读相关引擎、表演指导及两条文字示例；采用范围见[导演设计](directing.md#来源与适配范围) |
| [62656456 / AI Storyboard Director v5.2](https://github.com/62656456/ai-storyboard-director-v5.2/tree/a8d9ad6362ed38d76857199cb9ba92956f87ae5d) | 已接入观看终点、视觉主意、信息显露、切镜选择及事件线衔接 | 研读精编版相关决策与全量版部分内容；按当前任务调整结构、交付和表演规则 |

链接固定到本次核对的仓库版本，方便以后追溯。下面是针对个人指南整理的摘要与应用示例。外部成片和复测保留其已有验证状态；热度、验证模型与个人迁移结果分别记录。

## 1. 参考素材分工

借鉴 [LearnPrompt 的参考图身份锁定](https://github.com/LearnPrompt/awesome-seedance/blob/487c166e2f09487016452b90fec5e19a470af883/docs/templates/zh/character-reference-lock.md)。

多类素材同时上传时，用“实际素材标识 → 对象 → 控制属性 → 不采用属性”明确分工。身份、衣服、场景和构图可以来自不同图；标识沿用实际上传界面，不把资料里的命名示例当成平台通用语法。

本指南的应用示例：

| 素材 | 控制 | 不采用 |
| --- | --- | --- |
| 女生三视图 | 同一身份、五官、发型与比例 | 图板排版、白背景、站姿和原有神情 |
| 指定服装图 | 当前镜头的衣服结构与配饰 | 服装模特的身份和身材 |
| 客厅图 | 指定布局、陈设与光线 | 图中其他人物的身份 |

仅有一张角色参考时，不要求用户补齐其他素材。对应内容按本片结构放进素材、主体、造型、空间或摄影字段，必要时合写。主体数量按本片明确，例如一只橘猫和一只哈士奇各一只。

## 2. 喜剧从兑现笑点的时间倒推

借鉴 [LearnPrompt 的反转喜剧模板](https://github.com/LearnPrompt/awesome-seedance/blob/487c166e2f09487016452b90fec5e19a470af883/docs/templates/zh/meme-comedy.md)。

适用于靠反转或误会收尾的短片：先确定具体可见的笑点和发生时间，为对方的反应留出结尾空间，再安排观众理解误会所需的铺垫。停顿长短依据该片，不固定套用示例秒数。

应用到《狗打的》时，可先给猫扑向狗、狗惊讶反应分配时间，再向前安排敲头、猫回头、甩锅和看向狗。此处是候选规划方法，现存最终稿与案例状态不因此自动改变。

## 3. 逐镜复盘与局部修复

借鉴 [LearnPrompt 的制作与复盘流程](https://github.com/LearnPrompt/awesome-seedance/blob/487c166e2f09487016452b90fec5e19a470af883/agents/skills/seedance-production-workflow/SKILL.md)。需要比较或修复时，按时间记实际问题，仅调整对应镜头、素材或声音安排；尽可能保持相同生成设置，以便判断变化。具体记录格式见[反馈与维护](feedback.md)。

这项借鉴用于逐镜定位与局部修复。写提示词时选择适合当前类型和入口的结构，直接交付可用文本；成片反馈按用户需要提供。

## 应用前筛选

- [对白与表演模板](https://github.com/LearnPrompt/awesome-seedance/blob/487c166e2f09487016452b90fec5e19a470af883/docs/templates/zh/dialogue-performance-beats.md)含连续对白的静默限制。它不能覆盖含蓄情感戏的反应留白；《明天》的无声开口过程继续保留。
- [宠物模板](https://github.com/LearnPrompt/awesome-seedance/blob/487c166e2f09487016452b90fec5e19a470af883/docs/templates/zh/pet-animal.md)以单只动物抢镜为主要设定。借鉴数量与行为连续性时，改为本片实际数量，不限制猫狗双角色故事为一只动物。
- 时长、声音、动作、参考数量和镜头形式都以本次故事及实际平台入口为准。原稿若有空间、时间或运镜矛盾，应先调整；不把案例中的具体参数写成所有视频的能力保证。

## 转为个人经验

外部已验证提示词的具体写法可以按题材直接借鉴。采用这些写法的新片仍按[反馈流程](feedback.md)记录实际最终提示词、可见结果和用户反馈；案例说明链接到对应来源，并标明该次观察到的效果。持续反馈用于调整个人常用写法。
