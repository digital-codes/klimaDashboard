# Specs in card.json

## data

when using classes, first class entry indicates class column

```
    "data": [
      {
        "url": "https://transparenz.karlsruhe.de/dataset/7306d25b-8b18-445f-9351-6eec030c7753/resource/fd9de911-5142-4083-9d1b-5e09788022b3/download/treibhausgase.csv",
        "license": "CC-BY-4.0",
        "name": "Treibhausgasbilanz Karlsruhe",
        "expand": [url can point to list of urls. in that case, expand can be append (more rows), extend (more columns, requires join column), add (with columns list) or mean (with columns list)],
        "transpose": true/false,
        "skip":0,
        "format": "csv",
        "xaxis": "year",
        "columns": [
          "co2"
        ],
        "classes": [
          "category",
          "Private Haushalte",
          "Stadt",
          "Industrie",
          "Verkehr",
          "Gewerbe+Sonstiges"
        ]
      },
      {
        "url": "https://co2runter.karlsruhe.de/api/dashboard/footprints/",
        "license": "CC BY 4.0",
        "name": "CO2 Runter",
        "format": "json",
        "xaxis": "name",
        "columns": [
          "value"
        ],
        "classes": [
          "key"
        ]
      }
    ],
```

## chart 
    "chart": {
      "updating": false
    },


## controls

    "controls": {
      "range": {
        "present": false,
        "min": 1,
        "max": 100
      },
      "type": {
        "present": true,
        "options": [
          "line",
          "bar"
        ]
      },
      "stacked": {
        "present": true
      },
      "dataswitch": {
        "present": true
      },
      "animate": {
        "present": false
      }
    }

## extra

```
    "extra": [
      {
        "url": "https://transparenz.karlsruhe.de/dataset/ad0659b0-9e4b-408a-8840-3f19d5ec743d/resource/df843a83-b3f6-4929-b6a8-96471508f6f2/download/sensordaten_karlsruhe_bodentemperatur_bodenfeuchte_oct_2023.csv",
        "license": "CC BY 4.0",
        "name": "Sensoren  Friedrichsplatz 10/23",
        "format": "csv",
        "xaxis": "Datum",
        "columns": [
          "bodentemperatur"
        ],
        "classes": [
          "name",
          "SenseCap LBB (60) neu ✓",
          "SenseCap ECE (90) neu ✓"
        ]
      }
    ],

```
