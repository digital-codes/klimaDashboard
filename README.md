# Yet another Data Dashbaord
Configurable Dashbaord 

## What
Flexible dashboard to visualize data together with description

## Why
Many dashboard implementations exist. Mostly however tightly coupled to a specific use case or organization which makes porting difficult

## How
Vue3 web application with content structured in pages (views) with (multiple) tiles (cards). Each tile with 2 sections: descriptive text and corresponding visualization. 

Mutliple languages supported

Dark mode supported

## How to
### Text
Text input is markdown format, one file per tile per langage (en.md, de.md etc.). Support for teaser/more (collapsible or full page).

### Visualization
Variety of charts from [Apache Echarts library](https://echarts.apache.org), e.g. line, bar, tree, choropleth and [Leaflet maps](https://leafletjs.com/).

### Data
Data loaded from internal (same site) sources or external sources. Format: csv, json, geojson. Limited data preprocessing capabilites like column selection and class building. Sample (and simple) PHP proxy codes for CORS bypass and API access.

Typically, for statistical or timeseries data, one tile presents data for one or more parameters from a single source and with the same unit (like population statistics by age range over some year). Optionally, a tile may have a secondary dataset with topically related information (e.g. dataset-1 is energy consumption by sector, dataset-2 is energy distribution by source).

Custom data loaders per tile possible.

### Configuration
Configuration for each tile resides in one folder and made up from card.json for data related configuration, lang.json for tile specific localized string and the mentioned markdown files.

Examples

### Styling
Basic styling is applied through customizsation of style.scss and colors.scss

## Tooling
Vue3 with Vite, Vuestic-UI, Visualization libraries.

Clone repository: git clone <repo>

Install packages: npm i

Run devevlopment server: npm run dev

Open webpage (typically localhost:5173)


