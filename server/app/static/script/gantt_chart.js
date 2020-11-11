var data = [];
// var startTime = +new Date();
var categories = ['Python', 'C', '编码']

var types = [
    {name: 'Python', color: 'rgba(191, 122, 219, 1)'},
    {name: 'C', color: 'rgba(21, 93, 246, 1)'},
    {name: '编码', color: 'rgba(113, 249, 253, 1)'},
];

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

time_ranges = [
  {
    "end": 1592644908000,
    "id": 2020060200,
    "start": 1592644538000,
    "type_index": 1
  },
  {
    "end": 1592655166000,
    "id": 2020060201,
    "start": 1592652985000,
    "type_index": 1
  },
]


time_ranges.forEach(function(range){
    data.push({
        name: types[range.type_index].name,
        value: [
            range.type_index,
            new Date(range.start),
            new Date(range.end),
            (range.end - range.start)/1000,
            range.id
            // range.subtype_index
        ],
        itemStyle: {
            normal: {
                color: types[range.type_index].color
            }
        }
    })
});

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


function get_gantt_option() {
    option = {
        tooltip: {
            formatter: function (params){
                let total_seconds = params.value[3];
                let hms = seconds_to_hms(total_seconds);
                // subtype_name = subtypes[params.value[5]];

                return `${params.marker}${params.name}/${subtype_name}: ${duration_string}`;
            }
        },
        title: {
            text: 'Intervals in 2020-06-20',
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
            min: new Date('2020-06-20T00:00:00'),
            max: new Date('2020-06-21T00:00:00'),
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