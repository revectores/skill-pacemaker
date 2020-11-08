function get_knowledge_tree_option(tree) {
    console.log(tree.nodes)
    knowledge_tree_option = {
        title: {
        },
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
            {
                color: 'gray',
                type: 'graph',
                layout: 'none',
                symbolSize: 50,

                roam: false,
                label: {
                    fontSize: 15,
                    show: true
                },
                edgeSymbol: ['circle', 'arrow'],
                edgeSymbolSize: [4, 10],
                edgeLabel: {
                    fontSize: 40
                },
                data: tree.nodes,
                // links: [],
                links: tree.links,
                lineStyle: {
                    opacity: 0.9,
                    width: 2,
                    curveness: 0
                }
            }
        ]
    };
    return knowledge_tree_option;
}