## 分页面规范

### 页面跳转流程图

![](page_links.png)



### 菜单栏

“学习”, “社区”以及"用户"三栏，点击分别进入领域控制台页面`/domain/dashboard.html`, 社区主页`/community.html`以及用户信息页面`/user.html`. 菜单栏在所有页面的顶部（web端）或底部（移动端）显示.





### 主页

```yaml
name: index
url: /index.html
priority: -1
```

- 功能描述：用户登陆后进入的主页面.
- 内容：
    1. 若用户尚无可用的学习领域（通常出现在用户刚刚注册完成，或者所有领域都已经学习完成的情况），显示“选择新领域”按钮，点击跳转到新领域选择页面`/domain/select`, 否则显示“下一步”按钮. 点击继续上一次退出时正在进行的学习材料页面`/domain/[domain_name]/learn/[learn_id].html`或测试材料页面`/domain/[domain_name]/test/[test_id].html`.
    2. 个人信息流（包括日/周/月/年学习数据报表生成通知、提交学习材料同行评审进度、社区主题回复提醒等等）. 点击信息流中的特定条目则跳转到相应的页面.





### 领域控制台页面

```yaml
name: domain_dashboard
url: /domain/dashboard.html
priority: +35
```

- 功能描述：显示的当前正在学习的领域及其简单数据.
- 内容：
    1. 当前正在学习领域的一个列表，列出领域学习进程的简要数据. 点击某一学习领域所在的行即可进入相应的特定领域页面`/domain/[domain_name].html`. 只显示用户当前正在学习的领域.
    2. “学习新领域”按钮，点击进入新领域选择页面`/domain/select`.





### 新领域选择页面

```yaml
name: domain_select
url: /domain/select
priority: +20
```

- 功能描述：选择新的学习领域.
- 内容：

    1. 可供选择新领域的一个列表，列出领域的简要介绍. 点击某个领域进入到领域该概况页面`/domain/[domain_name]/intro.html`.
    2. 领域搜索框，根据关键词等条件搜索感兴趣的页面.





### 领域概况页面

```yaml
name: domain_intro
url: /domain/[domain_name]/intro.html
priority: +15
```

- 功能描述：显示特定领域的介绍.
- 内容：
    1. 特定领域的情况介绍文本.
    2. "开始学习”按钮，点击弹出确认框，确认后进入领域知识覆盖性测试流程.





### 特定领域页面

```yaml
name: domain
url: /domain/[domain_name].html
priority: +30
```

- 功能描述：特定领域的控制台. 显示用户在特定领域的详细数据.
- 内容：
    1. “下一步”按钮. 根据模型推荐的最优化学习路径，点击进入用户下一步应当进行的学习材料页面`/domain/[domain_name]/learn/[learn_id]`或测试材料页面`/domain/[domain_name]/test/[test_id].html`.
    2. 学习/测试路径树，包括已完成的部分和未完成的部分，点击树中的某一个结点可以进入这个结点所对应的的学习材料页面`/domain/[domain_name]/learn/[learn_id]`或测试材料页面`/domain/[domain_name]/test/[test_id].html`. 禁止进入尚未到达的学习或测试页面.
    3. 关于学习进度的各类统计图表，每个图表作为一个独立方块占据页面的一个部分. 点击可进入相应的图表详细信息页面`/graph/[graph_type]`.





### 学习页面

```yaml
name: learn
url: /domain/[domain_name]/learn/[learn_id].html
priority: +30
```

- 功能描述：学习材料内容显示.
- 内容：
    1. 学习材料显示区域.
    2. 计时器，统计当前内容学习时间、累计学习时间.
    3. “下一步”按钮，点击进入下一个学习材料页面或测试材料页面.





### 测试页面

```yaml
name: test
url: /domain/[domain_name]/test/[test_id].html
priority: +30
```

- 功能描述：测试内容显示与提交
- 内容：
    1. 测试问题显示区域.
    2. 测试选择、填空或代码上传区域.
    3. 计时器，统计当前测试进行时间、累计学习时间.
    4. “提交”按钮，点击提交答案并进入下一个学习材料或测试材料页面.





### 图表详细信息页面

```yaml
name: graph_info
url: /graph/[graph_type]
priority: -1
```





