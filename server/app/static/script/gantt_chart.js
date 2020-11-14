var data = [];
// var startTime = +new Date();

function leading_zero(string){
    return string.length < 2 ? '0' + string : string;
}

function seconds_to_hms(seconds){
    let hour = Math.floor(seconds / 3600);
    let minute = Math.floor(seconds % 3600 / 60);
    let second = seconds % 60;

    hour= leading_zero(hour.toString());
    minute = leading_zero(minute.toString());
    second = leading_zero(second.toString());

    duration_string = `${hour}:${minute}:${second}`;
    return duration_string;
}


/*
echarts.util.each(categories, function (category, index) {
    var baseTime = startTime;
    for (var i = 0; i < dataCount; i++) {
        var typeItem = types[index];
        var duration = Math.round(Math.random() * 10000);
        data.push({
            name: typeItem.name,
            value: [
                index,
                baseTime,
                baseTime += duration,
                duration
            ],
            itemStyle: {
                normal: {
                    color: typeItem.color
                }
            }
        });
        baseTime += Math.round(Math.random() * 2000);
    }
});*/


function renderItem(params, api) {
    var categoryIndex = api.value(0);
    var start = api.coord([api.value(1), categoryIndex]);
    var end = api.coord([api.value(2), categoryIndex]);
    var height = api.size([0, 1])[1] * 0.6;

    var rectShape = echarts.graphic.clipRectByRect({
        x: start[0],
        y: start[1] - height / 2,
        width: end[0] - start[0],
        height: height
    }, {
        x: params.coordSys.x,
        y: params.coordSys.y,
        width: params.coordSys.width,
        height: params.coordSys.height
    });

    return rectShape && {
        type: 'rect',
        shape: rectShape,
        style: api.style()
    };
}


function generate_gantt_option(logs, categories) {
    logs.forEach(function(log){
        console.log(log);
        data.push({
            name: log.domain_id,
            value: [
                log.domain_id - 1,
                new Date(log.start),
                new Date(log.end),
                (new Date(log.end) - new Date(log.start))/1000,
                log.id
                // range.subtype_index
            ],
            /*
            itemStyle: {
                normal: {
                    color: log.color
                }
            }*/
        })
    });

    option = {
        tooltip: {
            formatter: function (log_data){
                let total_seconds = log_data.value[3];
                let hms = seconds_to_hms(total_seconds);
                // subtype_name = subtypes[params.value[5]];

                return `${log_data.marker}${log_data.name}: ${hms}`;
            }
        },
        title: {
            text: '学习记录时间线',
            left: 'center'
        },
        dataZoom: [{
            type: 'slider',
            filterMode: 'weakFilter',
            showDataShadow: false,
            top: 400,
            height: 10,
            borderColor: 'transparent',
            backgroundColor: '#e2e2e2',
            handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7v-1.2h6.6z M13.3,22H6.7v-1.2h6.6z M13.3,19.6H6.7v-1.2h6.6z', // jshint ignore:line
            handleSize: 20,
            handleStyle: {
                shadowBlur: 6,
                shadowOffsetX: 1,
                shadowOffsetY: 2,
                shadowColor: '#aaa'
            },
            labelFormatter: ''
        }, {
            type: 'inside',
            filterMode: 'weakFilter'
        }],
        grid: {
            height: 300
        },
        xAxis: {
            min: new Date('2020-11-14T00:00:00'),
            max: new Date('2020-11-15T00:00:00'),
            type: 'time',
            scale: true,
            axisLabel: {
                /*
                formatter: function (val) {
                    return val
                }
                */
            }
        },
        yAxis: {
            data: categories
        },
        series: [{
            type: 'custom',
            renderItem: renderItem,
            itemStyle: {
                opacity: 0.8
            },
            encode: {
                x: [1, 2],
                y: 0
            },
            data: data
        }]
    };

    return option;
}