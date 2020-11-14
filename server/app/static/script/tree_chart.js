// time_ranges = [{"id": 2020060200, "type_index": 1, "subtype_index": 0, "start": 1592644538000, "end": 1592644908000}, {"id": 2020060201, "type_index": 1, "subtype_index": 0, "start": 1592652985000, "end": 1592655166000}, {"id": 2020060202, "type_index": 1, "subtype_index": 0, "start": 1592625587000, "end": 1592637018000}, {"id": 2020060203, "type_index": 1, "subtype_index": 0, "start": 1592637095000, "end": 1592640300000}, {"id": 2020060204, "type_index": 1, "subtype_index": 3, "start": 1592589532000, "end": 1592590158000}, {"id": 2020060205, "type_index": 1, "subtype_index": 3, "start": 1592621213000, "end": 1592621523000}, {"id": 2020060206, "type_index": 1, "subtype_index": 5, "start": 1592662861000, "end": 1592664307000}, {"id": 2020060207, "type_index": 3, "subtype_index": 10, "start": 1592640754000, "end": 1592642611000}, {"id": 2020060208, "type_index": 3, "subtype_index": 11, "start": 1592642615000, "end": 1592643093000}, {"id": 2020060209, "type_index": 3, "subtype_index": 11, "start": 1592624204000, "end": 1592625009000}, {"id": 2020060210, "type_index": 3, "subtype_index": 11, "start": 1592621018000, "end": 1592621525000}, {"id": 2020060211, "type_index": 3, "subtype_index": 12, "start": 1592590158000, "end": 1592618958000}, {"id": 2020060212, "type_index": 3, "subtype_index": 12, "start": 1592647504000, "end": 1592648442000}, {"id": 2020060213, "type_index": 3, "subtype_index": 12, "start": 1592587717000, "end": 1592589296000}, {"id": 2020060214, "type_index": 5, "subtype_index": 19, "start": 1592656389000, "end": 1592657140000}, {"id": 2020060215, "type_index": 5, "subtype_index": 19, "start": 1592623645000, "end": 1592624179000}, {"id": 2020060216, "type_index": 5, "subtype_index": 19, "start": 1592625012000, "end": 1592625584000}, {"id": 2020060217, "type_index": 5, "subtype_index": 19, "start": 1592643093000, "end": 1592643479000}, {"id": 2020060218, "type_index": 5, "subtype_index": 20, "start": 1592649054000, "end": 1592649223000}, {"id": 2020060219, "type_index": 5, "subtype_index": 20, "start": 1592650766000, "end": 1592651480000}, {"id": 2020060220, "type_index": 5, "subtype_index": 20, "start": 1592645659000, "end": 1592646588000}, {"id": 2020060221, "type_index": 5, "subtype_index": 20, "start": 1592623409000, "end": 1592623484000}, {"id": 2020060222, "type_index": 5, "subtype_index": 20, "start": 1592621749000, "end": 1592622649000}, {"id": 2020060223, "type_index": 5, "subtype_index": 20, "start": 1592656098000, "end": 1592656387000}, {"id": 2020060224, "type_index": 5, "subtype_index": 20, "start": 1592618958000, "end": 1592619188000}, {"id": 2020060225, "type_index": 5, "subtype_index": 21, "start": 1592623486000, "end": 1592623588000}, {"id": 2020060226, "type_index": 5, "subtype_index": 23, "start": 1592619205000, "end": 1592620345000}, {"id": 2020060227, "type_index": 5, "subtype_index": 23, "start": 1592650382000, "end": 1592650624000}, {"id": 2020060228, "type_index": 0, "subtype_index": 25, "start": 1592652350000, "end": 1592652980000}, {"id": 2020060229, "type_index": 0, "subtype_index": 25, "start": 1592623787000, "end": 1592623864000}, {"id": 2020060230, "type_index": 0, "subtype_index": 26, "start": 1592623868000, "end": 1592624177000}, {"id": 2020060231, "type_index": 0, "subtype_index": 27, "start": 1592649276000, "end": 1592650164000}, {"id": 2020060232, "type_index": 0, "subtype_index": 27, "start": 1592651481000, "end": 1592652341000}, {"id": 2020060233, "type_index": 0, "subtype_index": 27, "start": 1592621165000, "end": 1592621195000}, {"id": 2020060234, "type_index": 0, "subtype_index": 27, "start": 1592650184000, "end": 1592650335000}, {"id": 2020060235, "type_index": 4, "subtype_index": 33, "start": 1592655864000, "end": 1592656089000}, {"id": 2020060236, "type_index": 6, "subtype_index": 41, "start": 1592621641000, "end": 1592621739000}, {"id": 2020060237, "type_index": 6, "subtype_index": 41, "start": 1592657983000, "end": 1592662856000}, {"id": 2020060238, "type_index": 6, "subtype_index": 41, "start": 1592622654000, "end": 1592623143000}, {"id": 2020060239, "type_index": 6, "subtype_index": 41, "start": 1592643714000, "end": 1592644529000}, {"id": 2020060240, "type_index": 6, "subtype_index": 41, "start": 1592646681000, "end": 1592647501000}, {"id": 2020060241, "type_index": 6, "subtype_index": 41, "start": 1592655493000, "end": 1592655864000}, {"id": 2020060242, "type_index": 6, "subtype_index": 41, "start": 1592620371000, "end": 1592620758000}]


function seconds_to_hms(seconds){
    let hour = Math.floor(seconds / 3600);
    let minute = Math.floor(seconds % 3600 / 60);
    let second = seconds % 60;

    hour = leading_zero(hour.toString());
    minute = leading_zero(minute.toString());
    second = leading_zero(second.toString());

    duration_string = `${hour}:${minute}:${second}`;
    return duration_string;
}


function types_tree(intervals, types, subtypes, types2subtypes){
    let tree = {'name': 'root', 'children': []};

    total_duration = 0;

    type_durations = {};
    subtype_durations = {};
    types.forEach((type) => {
        type_durations[type] = 0;
    });
    subtypes.forEach((subtype) => {
        subtype_durations[subtype] = 0;
    });

    intervals.forEach(function(interval){
        let duration = (interval.end - interval.start) / 1000;
        console.log(interval, duration);
        type_durations[interval.type_name] += duration;
        subtype_durations[interval.subtype_name] += duration;
        total_duration += duration;
    });

    console.log('subtype_durations:', subtype_durations);
    console.log('type_durations:', type_durations);
    for (let type_name in types2subtypes){
        let type_node = {
            "name": type_name,
            "children": [],
            "value": type_durations[type_name],
            "itemStyle": {
                "opacity": type_durations[type_name] ? 1 : 0.3
            }
        };

        types2subtypes[type_name].forEach(function(subtype_name){
            let children_node = {
                "name": subtype_name,
                "value": subtype_durations[subtype_name],
                "itemStyle": {
                    "opacity": subtype_durations[subtype_name]? 1 : 0.3
                },
            };
            type_node["children"].push(children_node);
        });

        tree['children'].push(type_node);
    }
    return tree;
}



function types_tree_with_existence(intervals){
    let tree = {'name': 'root', 'children': []};
    for (let key in types_to_subtypes){
        let type_node = {"name": types[key], "children": []};
        types_to_subtypes[key].forEach(function(subtype_index){
            let children_node = {"name": subtypes[subtype_index], "value": 0};
            type_node["children"].push(children_node);
        });
        tree['children'].push(type_node);
    }
    return tree;
}


function get_tree_chart(logs, types, subtypes, type2subtypes) {
    let data = types_tree(logs, types, subtypes, type2subtypes);

    let option = {
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove'
        },
        title: {
            text: '学习记录树状图',
            left: 'center'
        },
        series: [
            {
                type: 'tree',
                id: 0,
                name: 'tree1',
                data: [data],

                top: '10%',
                left: '8%',
                bottom: '22%',
                right: '20%',

                symbolSize: 7,

                // edgeShape: 'polyline',
                edgeForkPosition: '63%',
                initialTreeDepth: 3,

                lineStyle: {
                    width: 2
                },

                label: {
                    backgroundColor: '#fff',
                    position: 'left',
                    verticalAlign: 'middle',
                    align: 'right',
                    formatter: function(node){
                        return node.value ? `${node.name} ${seconds_to_hms(node.value)}`: node.name;
                    }
                },

                leaves: {
                    label: {
                        position: 'right',
                        verticalAlign: 'middle',
                        align: 'left',
                        formatter: function(node){
                            return node.value ? `${node.name} ${seconds_to_hms(node.value)}`: node.name;
                        }
                    },
                },

                expandAndCollapse: true,
                animationDuration: 550,
                animationDurationUpdate: 750
            }
        ]
    };

    return option;
}
