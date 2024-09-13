// Function to download data as CSV
function downloadDataAsCSV(data) {
    const x = data.x;
    const csvCols = [data.xLabel]
    const csvRows = []
    data.cols.forEach(col => {csvCols.push(col.name)})
    csvRows.push(csvCols.join(';'))
    // data rows
    x.forEach((value,index) => {
        const row = [value]
        data.cols.forEach(series => {
            row.push(series.data[index])
        })
        csvRows.push(row.join(';'))
    })
    // blob
    const csvContent = csvRows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    return url;
}

// Function to download data as JSON
function downloadDataAsJSON(data) {
    const x = data.x;
    const columnNames = []
    data.cols.forEach(col => {columnNames.push(col.name)});
    console.log(columnNames);
    return
}

export { downloadDataAsCSV, downloadDataAsJSON };
