// echarts utilities besides color/symbols config which are elsewhere
// https://www.data-forge-js.com/
// https://github.com/data-forge/data-forge-ts/blob/master/docs/guide.md
//import * as dataForge from 'data-forge'

// custom dataframe library
import DataFrame from "dflib"

import getDataSymbol from '@/composables/DataSymbol';

const setType = (type, options) => {
  for (let idx = 0; idx < options.series.length; idx++) {
    options.series[idx].type = type
    if (type == "bar") {
      options.series[idx].itemStyle = {
        decal:
        {
          dashArrayX: 5,
          dashArrayY: 1,
          rotation: getDataSymbol(idx).pattern,
          color: "#000",
        }
      }
    } else {
      options.series[idx].itemStyle = {}
    }
  }
}

const setStacked = (stacked, options) => {
  for (let idx = 0; idx < options.series.length; idx++) {
    options.series[idx].stack = stacked ? 'stack' : null
  }
}


// default options for line and bar charts
const lineBarDefaults = (name = "Default Name", labelX = "", labelY = "", locale = "de") => {
  const defaults = {
    //darkMode: "auto",
    aria: {
      enabled: true,
      label: {
        enabled: true,
        // description: "123", // name,
      }
    },
    // grid settings allow to control the position of the chart
    // usefull to increase label space on mobile
    // initialize to 10% here. use 20% on mobile
    grid: [
      {
        left: "10%",
      }
    ],
    tooltip: {
      trigger: 'axis',
      valueFormatter: (value) => value != null ? Intl.NumberFormat(locale, { maximumFractionDigits: 1 }).format(value) : "N/A",
      //valueFormatter: (value) => value != null ? value.toFixed(1) : "N/A",
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
    // backgroundColor: "#333",
    xAxis: {
      animation: false,
      name: labelX, //"X-axis",
      nameLocation: "center",
      nameGap: 30,
      boundaryGap: true,
      axisLabel: {
        "show": true,
        //formatter: '{value} [Unit-X]'
      },
      type: "category",
      //data: dummyData.map((item) => item.date),
    },
    yAxis: {
      animation: false,
      name: labelY, //"Y-axis",
      type: "value",
      nameLocation: "end",
      nameGap: 10,
      top: "top",
      //offset:-30,
      axisLabel: {
        margin: 1, // 1 on mobile, 10 else
        show: true,
        hideOverlap: true,
        interval: 0,
        // width: 190,
        //formatter: '{value} [Unit-Y]'
        formatter: v => Intl.NumberFormat(lang).format(v)
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
  if (data == null) {
    return null;
  }
  if (typeof data === 'number') {
    return data;
  } else {
    return parseFloat(data.replace(",", "."));
  }
}

const updateEchartsOptions = async (chartOptions, data, dataX, classList,
  columnList, type, stacked, size = "large", locale = "de") => {
  //console.log("Updating from data:", data);
  // we have to know if we get 1 or 2 series from data.
  // assume we always have an array. 
  // in case the inner data is an array too, we have multiple series
  // let df = new dataForge.DataFrame(data)
  let df = new DataFrame(data)
  // console.log("dflib:",df.toArray())
  //console.log(df.toString())
  //console.log("Dataframe:", df.head(3).toString());
  // let cols = df.getColumnNames()
  let cols = df.columnNames()
  // console.log("Cols:", cols)

  if (cols.length == 0) {
    // console.log("No columns");
    cols = Object.keys(data)
    // // console.log("Keys:", cols);
    if (cols.length == 0) {
      // console.log("Again no columns")
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

    // df = new dataForge.DataFrame(tabularData);
    df = new DataFrame(tabularData);
    // console.log("dflib:",df.toArray())
    // df = new dataForge.DataFrame(data[keys[0]])
    //console.log("Dataframe:", df.toString());
  }

  // input differs by identifiers for category (X-axis), value (Y-Axis), group
  // and selected group names
  let seriesData

  if (dataX == "") {  // no X-axis given 
    // console.log("No X-Axis")
    return chartOptions
  }
  // // console.log("X-Axis:", dataX)

  // convert timestamp for energy-charts timeseries data
  // SPECIAL - ENERGYCHARTS
  if (dataX == "unix_seconds") {
    // Unix timestamp in seconds
    // Convert to milliseconds (JavaScript timestamps are in milliseconds)
    /*
    const date = new Date(unixTimestamp * 1000);
    // Convert to ISO format
    const isoString = date.toISOString();
    */
    // Create a new column 'iso_datetime' based on the 'unix_timestamp' column
    /*
    df = df.withSeries('iso_datetime', df.getSeries('unix_seconds').select(unix_seconds => 
      new Date(unix_seconds * 1000).toISOString()
    )); 
    */

    // get seconds colummn
    // console.log("x",df.toJSON())
    const unix_seconds = df.selectCols(['unix_seconds']).toArray(false)
    // console.log("Unix Seconds:", unix_seconds)
    const iso_datetime = unix_seconds.map(item => new Date(item * 1000).toISOString())
    // console.log("ISO Datetime:", iso_datetime)
    df.addColumn('iso_datetime', iso_datetime)
    // console.log("dflib:",df.toJSON())

    dataX = 'iso_datetime'
    // // console.log("Converted timestamp:", df.head(3).toString());
  }

  const chartData = df.toJSON() //df.toArray();
  // console.log("Chart Data:", chartData)
  // console.log("X:", dataX)
  let categories = chartData.map(item => item[dataX]).filter((value, index, self) => self.indexOf(value) === index);
  categories = categories.filter(category => ((category !== null) && (category !== undefined)));
  // console.log("Categories:", categories, categories.length) 

  if (typeof categories[0] === 'number') {
    //console.log("Sorting categories", categories)
    categories.sort((a, b) => a - b)
  }

  let classes = []
  // filter classes
  if (classList && Array.isArray(classList) && classList.length > 0) {
    const classId = classList[0]
    //console.log("Filtering by classes on:", classId)
    if (classList.length > 1) {
      classes = classList.slice(1)
    } else {
      // classes = df.getSeries(classId).distinct().toArray()
      classes = df.unique(classId)
    }
    // console.log("Filtering classes:", classes)
    seriesData = chartData.filter(item => classes.includes(item[classId]));
    // console.log("Filtered Data:", seriesData)
  } else {
    seriesData = chartData;
  }

  let columns = []
  if (columnList && Array.isArray(columnList) && columnList.length > 0) {
    columns = columnList
  } else {
    //console.log("No columns given")
    // columns = df.getColumnNames()
    columns = df.columnNames()
  }
  //console.log("Initial  columns:", columns)
  /*
  let itemStyle = null
  if (type == "bar") {
    itemStyle =
    {
      decal:
      {
        dashArrayX: 5,
        dashArrayY: 1,
        rotation: getDataSymbol(index).pattern,
        color: "#000",
      }
    }
  }
  */

  // don't exclude class name from columns here
  const excludeCols = [dataX]
  // // console.log(" Excluding columns:", excludeCols)
  // instead, include the class column here
  const includedColumns = columns.filter(column => !(excludeCols.includes(column)))
  if (classList && Array.isArray(classList) && classList.length > 0) {
    includedColumns.push(classList[0])
  }
  // // console.log("Included columns:", includedColumns) // DROP

  // series created from either classes or columns
  // if length of classes > 1 we have multiple series and length of columns must be 1
  // if length of columns > 1 we have multiple series and length of classes must be 1

  // // console.log("Classes:", classes, "Columns:", includedColumns)

  if (classes.length >= 1) {
    // // console.log("Creating series from classes")
    // create names from classes
    seriesData = classes.map((name, index) => {
      // // console.log("Name:",name,", Index:",index) // DROP
      const filteredData = chartData.filter(item => item[classList[0]] === name);
      // // console.log("Filtered Data:", filteredData) // DROP
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
        itemStyle: type == "bar" ? {
          decal:
          {
            dashArrayX: 5,
            dashArrayY: 1,
            rotation: getDataSymbol(index).pattern,
            color: "#000",
          }
        } : {},
      };
    });
  } else {
    // create names from columns
    // // console.log("Creating series from columns:", includedColumns)
    // if we have classes, remove the corresponding column from included columns
    const valueColumns = classes.length > 0 ? includedColumns.filter(item => item != classList[0]) : includedColumns
    seriesData = valueColumns.map((column, index) => {
      //console.log("Column:",column)
      //console.log("Categories:",categories) 
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
        itemStyle: type == "bar" ? {
          decal:
          {
            dashArrayX: 5,
            dashArrayY: 1,
            rotation: getDataSymbol(index).pattern,
            color: "#000",
          }
        } : {},
      };
    });
  }

  // update yaxis margin
  if (size == "large") {
    chartOptions.yAxis.axisLabel.margin = 10
  } else {
    chartOptions.yAxis.axisLabel.margin = 10
  }
  // update locale
  chartOptions.yAxis.axisLabel.formatter = (v) => Intl.NumberFormat(locale).format(v)
  chartOptions.tooltip.valueFormatter = (value) => value != null ? Intl.NumberFormat(locale, { maximumFractionDigits: 1 }).format(value) : "N/A"


  // // console.log("Final Series:", seriesData)

  chartOptions.xAxis.type = "category"
  chartOptions.xAxis.data = categories
  chartOptions.series = seriesData
  // grid settings allow to control the position of the chart
  // usefull to increase label space on mobile
  // unset or 10% normally, 20% on mobile
  chartOptions.grid[0].left = size == "small" ? "20%" : "10%"

  //console.log("Options updated:", chartOptions);
  return chartOptions
}



export { lineBarDefaults, updateEchartsOptions, setType, setStacked }

