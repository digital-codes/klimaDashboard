// echarts utilities besides color/symbols config which are elsewhere
// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md
import * as dataForge from 'data-forge'

import getDataSymbol from '@/composables/DataSymbol';

// default options for line and bar charts
const lineBarDefaults = (name = "Default Name") => {
    const defaults = {
    //darkMode: "auto",
    tooltip: {
      trigger: 'axis',
      valueFormatter: (value) => value != null ? value.toFixed(1) : "N/A",
      /*
      axisPointer: {
        type: 'cross',
        label:{
          show: true,
        }
      },
      */
    },
    toolbox: {
      show: true,
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        //dataView: { readOnly: true },
        //magicType: { type: ['line', 'bar', 'stack'] },
        //restore: {},
      }
    },
    title: {
      "show": true,
      "left": "center",
      "text": name,
      "textStyle": {
        //"color": "#0f0",
        "fontSize": 20
      }
    },
    legend: {
      right: 'auto',
      top: 'bottom',
      show: true,
      type: 'scroll',
    },
    "aria": {
      "enabled": true,
      "description": name,
      show: true,
    },
    // backgroundColor: "#333",
    xAxis: {
      name: "X-axis",
      nameLocation: "center",
      nameGap: 30,
      boundaryGap: true,
      axisLabel: {
        "show": true
        //formatter: '{value} [Unit-X]'
      },
      type: "category",
      //data: dummyData.map((item) => item.date),
    },
    yAxis: {
      name: "Y-axis",
      type: "value",
      nameLocation: "end",
      nameGap: 10,
      top: "top",
      //offset:-10,
      axisLabel: {
        margin: 10, // smaller on mobile
        show: true,
        hideOverlap: true,
        interval: 0,
        //formatter: '{value} [Unit-Y]'
      },
      type: "value",
    },
    series: []
  }
  return defaults
}

// default data handling for line and bar charts
// helper function
const parseData = (data) => {
    if (typeof data === 'number') {
      return data;
    } else {
      return parseFloat(data.replace(",", "."));
    }
  }
  
const updateEchartsOptions = async (chartOptions, data, dataX, classList, columnList, type, stacked) => {
    console.log("Updating from data:", data);
    // we have to know if we get 1 or 2 series from data.
    // assume we always have an array. 
    // in case the inner data is an array too, we have multiple series
    let df = new dataForge.DataFrame(data)
    //console.log(df.toString())
    //console.log("Dataframe:", df.head(3).toString());
    let cols = df.getColumnNames()
    console.log("Cols:", cols)
  
    if (cols.length == 0) {
      console.log("No columns");
      cols = Object.keys(data)
      console.log("Keys:", cols);
      if (cols.length == 0) {
        console.log("Again no columns")
        return chartOptions
      }
      const tabularData = [];
      for (const key of cols) {
        const items = data[key];
        for (const item of items) {
          item.key = key;
          tabularData.push(item);
        }
      }
  
      df = new dataForge.DataFrame(tabularData);
      // df = new dataForge.DataFrame(data[keys[0]])
      // console.log("Dataframe:", df.toString());
    }
  
    // input differs by identifiers for category (X-axis), value (Y-Axis), group
    // and selected group names
    let seriesData
  
    if (dataX == "") {  // no X-axis given 
      console.log("No X-Axis")
      return chartOptions
    }
    console.log("X-Axis:", dataX)
  
    const chartData = df.toArray();
    let categories = chartData.map(item => item[dataX]).filter((value, index, self) => self.indexOf(value) === index);
    categories = categories.filter(category => category !== null);
    //console.log("Categories:", categories, categories.length)
  
    let classes = []
    // filter classes
    if (classList && Array.isArray(classList) && classList.length > 0) {
      const classId = classList[0]
      //console.log("Filtering by classes on:", classId)
      if (classList.length > 1) {
        classes = classList.slice(1)
      } else {
        classes = df.getSeries(classId).distinct().toArray()
      }
      //console.log("Filtering classes:", classes)
      seriesData = chartData.filter(item => classes.includes(item[classId]));
  
    } else {
      seriesData = chartData;
    }
  
    // console.log("Filtered classes:", seriesData)
  
    let columns = []
    if (columnList && Array.isArray(columnList) && columnList.length > 0) {
      columns = columnList
    } else {
      //console.log("No columns given")
      columns = df.getColumnNames()
    }
    //console.log("Initial  columns:", columns)
  
    // don't exclude class name from columns here
    const excludeCols = [dataX]
    // console.log(" Excluding columns:", excludeCols)
    // instead, include the class column here
    const includedColumns = columns.filter(column => !(excludeCols.includes(column)))
    if (classList && Array.isArray(classList) && classList.length > 0) {
      includedColumns.push(classList[0])
    }
    // console.log("Included columns:", includedColumns)
  
    // series created from either classes or columns
    // if length of classes > 1 we have multiple series and length or columns must be 1
    // if length of columns > 1 we have multiple series and length or classes must be 1
    if (classes.length > 1) {
      console.log("Creating series from classes")
      // create names from classes
      seriesData = classes.map((name, index) => {
        //console.log("Name:",name,", Index:",index)
        const filteredData = chartData.filter(item => item[classList[0]] === name);
        //console.log("Filtered Data:", filteredData)
        return {
          name: name,
          //data: filteredData.map(item => parseData(item[columnList[0]])),
          data: categories.map(position => {
            //console.log("Position:",position)
            if (filteredData.find(item => item[dataX] === position) == null) {
              return null
            } else {
              return parseData(filteredData.find(item => item[dataX] === position)[columnList[0]])
            }
          }),
          type: type,
          stack: stacked ? 'stack' : null,
          symbol: getDataSymbol(index).symbol,
          color: getDataSymbol(index).color,
          symbolSize: 16,
          label: {
            show: false,
            position: 'top',
            color: 'black',
            fontSize: 12,
          },
          itemStyle:
          {
            decal:
            {
              dashArrayX: 5,
              dashArrayY: 1,
              rotation: getDataSymbol(index).pattern,
              color: "#000",
            }
          }
        };
      });
    } else {
      // create names from columns
      console.log("Creating series from columns")
      // if we have classes, remove the corresponding column from included columns
      const valueColumns = classes.length > 0 ? includedColumns.filter(item => item != classList[0]) : includedColumns
      seriesData = valueColumns.map((column, index) => {
        //console.log("Column:",column)
        return {
          name: column,
          data: categories.map(position => {
            //console.log("Position:",position)
            const item = chartData.find(item => item[dataX] === position)
            if (item == null) {
              //console.log("No data for position:",position)
              return null
            } else {
              //console.log("Data at position:",position,item)
              return parseData(chartData.find(item => item[dataX] === position)[column])
            }
          }),
          type: type,
          stack: stacked ? 'stack' : null,
          symbol: getDataSymbol(index).symbol,
          color: getDataSymbol(index).color,
          symbolSize: 16,
          label: {
            show: false,
            position: 'top',
            color: 'black',
            fontSize: 12,
          },
          itemStyle:
          {
            decal:
            {
              dashArrayX: 5,
              dashArrayY: 1,
              rotation: getDataSymbol(index).pattern,
              color: "#000",
            }
          }
        };
      });
    }
  
    // console.log("Final Series:", seriesData)
  
    chartOptions.xAxis.type = "category"
    chartOptions.xAxis.data = categories
    chartOptions.series = seriesData
    //console.log("Options updated:", chartOptions);
    return chartOptions
  }



export { lineBarDefaults, updateEchartsOptions }

