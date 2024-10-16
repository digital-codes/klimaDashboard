import * as echarts from 'echarts';

var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

option = {
  tooltip: {
    formatter: function (info) {
      var value = info.value;
      var treePathInfo = info.treePathInfo;
      var treePath = [];
      for (var i = 1; i < treePathInfo.length; i++) {
        treePath.push(treePathInfo[i].name);
      }
      return [
        '<div class="tooltip-title">' +
          echarts.format.encodeHTML(treePath.join('/')) +
          '</div>',
        'Value: ' + echarts.format.addCommas(value) + ' KB'
      ].join('');
    }
  },
  series: [
    {
      type: 'treemap',
      itemStyle: {
        borderColor: '#707',
        borderWidth: 2,
        gapWidth: 5
      },
      label: {
        show: true,
        formatter: '{b}\n{c}'
      },
      data: [
        {
          name: 'nodeA',
          value: 10,
          upperLabel: {
            show: true,
            height: 30
          },
          children: [
            {
              name: 'nodeAa',
              value: 4
            },
            {
              name: 'nodeAb',
              value: 6
            }
          ]
        },
        {
          name: 'nodeB',
          upperLabel: {
            show: true,
            height: 30
          },
          children: [
            {
              name: 'nodeBa',
              children: [
                {
                  name: 'nodeBa1',
                  value: 8
                },
                {
                  name: 'nodeBa2',
                  children: [
                    {
                      name: 'nodeBa2a1',
                      value: 3
                    },
                    {
                      name: 'nodeBa2a2',
                      value: 1
                    }
                  ]
                },
                {
                  name: 'nodeBa2',
                  value: 4
                }
              ]
            }
          ]
        }
      ]
    }
  ]
};

option && myChart.setOption(option);
