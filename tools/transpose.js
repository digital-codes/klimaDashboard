import forge from "data-forge"
import axios from "axios"

/*
forge = require("data-forge")
axios = require("axios")
*/


axios.get("http://localhost:5173/data/karlsruhe/KA_Strom_Gas_Jahr.csv").then((result) => {
    const rawCsv = result.data
    console.log(result.status)
    // first row is description. Drop!
    const csv = (rawCsv.split("\n").splice(1)).join("\n")
    // console.log(csv)
    const df = forge.fromCSV(csv)
    console.log(df.head(3).toString())

    const transposedData = [];
    for (let i = 1; i < df.getColumnNames().length; i++) {
        const year = df.getColumnNames()[i];
        for (let j = 0; j < df.toRows().length; j++) {
            const category = df.toRows()[j][0];
            const value = df.toRows()[j][i];
            transposedData.push({ Jahr: year, Category: category, Value: value });
        }
    }
    // console.log(transposedData);
    const dfTransposed = new forge.DataFrame(transposedData);
    console.log(dfTransposed.toString());

    const csvT = dfTransposed.toCSV();
    console.log(csvT);

})


