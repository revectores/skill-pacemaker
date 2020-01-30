from graphviz import Source, render

source = """
digraph {
    dpi = 300;
    
    
    index [label="主页"]
    domain_dashboard [label="领域控制台页面"]
    domain_select [label="新领域选择页面"]
    domain_intro [label="领域概况页面"]
    domain [label="特定领域页面"]
    learn [label="学习页面"]
    test [label="测试页面"]
    graph_info [label="图表详细信息页面"]
    community [label="社区主页"]


    {rank = same; learn; test;}


    index -> domain_dashboard
    index -> community
    
    domain_dashboard -> domain
    domain_dashboard -> domain_select
    domain_select -> domain_intro
    domain -> graph_info
    domain -> learn
    domain -> test
    learn -> test
    test -> learn
}
"""

dot = Source(source)
dot.render('life', view=True, format='png')
