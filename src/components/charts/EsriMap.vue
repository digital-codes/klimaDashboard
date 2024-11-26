<template>
  <div class="container">
    <div class="map" ref="theMap"></div>
    <div ref="logoDiv" class="esri-widget">
      <img src="/icons/favicon.svg" class="esrilogo" alt="Logo" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";

//import "./esri.css";

/* dynamic bundlin below seems to save about 500kB. not very much .... to be confimed */
import Map from "@arcgis/core/Map";
import MapView from "@arcgis/core/views/MapView";
/* */
import VectorTileLayer from "@arcgis/core/layers/VectorTileLayer";
import GraphicsLayer from "@arcgis/core/layers/GraphicsLayer";
import Graphic from "@arcgis/core/Graphic";
import PictureMarkerSymbol from "@arcgis/core/symbols/PictureMarkerSymbol";

import FeatureLayer from "@arcgis/core/layers/FeatureLayer";

import Polyline from "@arcgis/core/geometry/Polyline";
import { SimpleLineSymbol } from "@arcgis/core/symbols";

import PopupTemplate from "@arcgis/core/PopupTemplate";

import LayerList from "@arcgis/core/widgets/LayerList";
import Home from "@arcgis/core/widgets/Home";
import Expand from "@arcgis/core/widgets/Expand";

import "@arcgis/coding-components/dist/arcgis-coding-components/arcgis-coding-components.css";
import "@esri/calcite-components/dist/calcite/calcite.css";
import "@arcgis/core/assets/esri/themes/light/main.css";



const emit = defineEmits(["data"]);

const props = defineProps({
  /* Add your props here */
  dataUrl: {
    // basemap url
    type: String,
    required: true,
  },
  poiUrl: {
    type: String,
    default: null // "/data/karlsruhe/weatherPois.json",
  },
  featureUrl: {
    type: String,
    default: null // "/data/karlsruhe/plz.geojson"
  },
  dataName: {
    type: String,
    default: "VectorMap",
  },
  ariaLabel: {
    type: String,
    default: "Vector Map",
  },
  // optional X axis identifier
  dataX: {
    type: String,
    default: "",
  },
  // optional Y axis identifier
  dataY: {
    type: String,
    default: "",
  },
  // optional X axis label
  labelX: {
    type: String,
    default: "",
  },
  // optional Y axis label
  labelY: {
    type: String,
    default: "",
  },
  // optional format
  dataFormat: {
    type: String,
    default: "json",
  },
  // optional format
  dataDelimiter: {
    type: String,
    default: ";",
  },
  // optional columns to be selected
  dataProps: {
    type: Object,
    default: { "name": "name", "url": "url", "attribution": "attribution", "description": "description" },
  },
  locale: {
    type: String,
    default: "de",
  },
});

//const mapInstance = ref(null);
//const viewInstance = ref(null);

let mapInstance = null
let viewInstance = null;
const logoDiv = ref(null);
const theMap = ref(null);


let tileLayer = null; // map tiles
let featureLayer = null; // geojson layer for features
let poiLayer = null; // point of interest layer, geojson
const featureData = ref(null); // geojson layer for features
const poiData = ref(null); // point of interest layer, geojson



watch(() => props.dataUrl, async (newVal, oldVal) => {
  console.log("Data URL changed", newVal, oldVal);
  await loadData();
});
watch(() => props.poiUrl, async (newVal, oldVal) => {
  console.log("POI URL changed", newVal, oldVal);
  //await loadData();
});
watch(() => props.featureUrl, async (newVal, oldVal) => {
  console.log("Feature URL changed", newVal, oldVal);
  //await loadData();
});

const addPoi = (longitude, latitude, title, content) => {
  var point = {
    type: "point", // autocasts as new Point()
    longitude: longitude,
    latitude: latitude
  };
  var markerSymbol = new PictureMarkerSymbol({
    url: "/icons/oklab.svg",  // Path to your custom icon
    width: "32px", // Adjust size as needed
    height: "32px",
    // Optionally, set an anchor point to position the icon correctly
    yoffset: 16 // Moves the icon up by half its height
  });
  var pointGraphic = new Graphic({
    geometry: point,
    symbol: markerSymbol,
    popupTemplate: { // autocasts as new PopupTemplate()
      title: title,
      content: content
    }
  });
  return pointGraphic;
}

const createPoiLayer = (data) => {
  // create the layer
  if (poiLayer)
    poiLayer.removeAll();
  else {
    poiLayer = new GraphicsLayer(
      {
        title: "Points of Interest",
        visible: true
      }
    );
  }
  // add the points

  console.log("pois", data.features);
  data.features.forEach(point => {
    const coords = point.geometry.coordinates;
    const props = point.properties;
    let content = props.name;
    const title = props.name;
    if (props.img && props.img.length > 0) {
      if (props.img.startsWith("http")) {
        content = `<div class='popup-content'><h4>${props.name}</h4><img src="${props.img}" alt='Supported' style='width: 100px;'><p>${props.attribution}</p></div>`
      } else {
        content = `<div class='popup-content'><h4>${props.name}</h4><img src="${assetPathUrl}/${props.img}" alt='Supported' style='width: 100px;'><p></p></div>`
      }
    }
    const poi = addPoi(coords[0], coords[1], title, content);
    poiLayer.add(poi);
  });
  return poiLayer;
}

const plzFeaturePreps = (data) => {
  const plzFeatures = data.features.map((feature, index) => {
      return {
        geometry: {
          type: feature.geometry.type.toLowerCase(), // e.g., "polygon"
          rings: feature.geometry.coordinates[0], // Coordinates for polygon
        },
        attributes: {
          ...feature.properties,
          OBJECTID: index + 1, // Generate OBJECTID for Esri FeatureLayer
        },
      };
    });

    // Define the fields for the FeatureLayer
    const plzFields = [
      {
        name: "OBJECTID",
        alias: "Object ID",
        type: "oid",
      },
      {
        name: "PLZ",
        alias: "Postal Code",
        type: "string",
      },
      {
        name: "SHAPE_Area",
        alias: "Shape Area",
        type: "double",
      },
    ];

    // Define color mapping for the PLZs
    const colorMap = {
      "76131": [255, 0, 0, 0.1],    // Red
      "76133": [0, 255, 0, 0.1],    // Green
      "76135": [0, 0, 255, 0.1],    // Blue
      "76137": [255, 255, 0, 0.1],  // Yellow
      "76139": [255, 0, 255, 0.1],  // Magenta
      "76141": [0, 255, 255, 0.1],  // Cyan
      "76149": [128, 0, 128, 0.1],  // Purple
      "76187": [255, 165, 0, 0.1],  // Orange
      "76199": [0, 128, 128, 0.1],  // Teal
      "76227": [128, 128, 0, 0.1],  // Olive
      "76228": [128, 0, 0, 0.1],    // Maroon
      "76229": [0, 128, 0, 0.1],    // Dark Green
      "76275": [0, 0, 128, 0.1],    // Navy
      "76297": [192, 192, 192, 0.1], // Silver
      "76307": [105, 105, 105, 0.1], // Dim Gray
      "76185": [105, 70, 105, 0.1], // 
      "76189": [60, 70, 135, 0.1], // 
    };

    // Create unique value renderer
    const uniqueValueInfos = Object.keys(colorMap).map((plz) => ({
      value: plz,
      symbol: {
        type: "simple-fill",
        color: colorMap[plz], // Color from the color map
        outline: {
          color: [0, 0, 0], // White outline
          width: 2,
        },
      },
      label: `PLZ: ${plz}`,
    }));

    const renderer = {
      type: "unique-value",
      field: "PLZ", // Field to match
      uniqueValueInfos: uniqueValueInfos,
      defaultSymbol: {
        type: "simple-fill",
        color: [200, 200, 200, 0.4], // Default gray for unmatched
        outline: {
          color: [255, 255, 255],
          width: 1,
        },
      },
      defaultLabel: "Other PLZs",
    };

    // Create the FeatureLayer
    const plzFeatureLayer = new FeatureLayer({
      title: "PLZ",
      visible: false, // start invisible
      source: plzFeatures, // GeoJSON features as Esri Graphics
      fields: plzFields,
      objectIdField: "OBJECTID", // Required for Esri FeatureLayer
      geometryType: "polygon", // Geometry type
      renderer: renderer, // Unique value renderer
      popupTemplate: {
        title: "PLZ: {PLZ}",
        content: `
                        <ul>
                            <li><b>Fläche:</b> {SHAPE_Area} m²</li>
                        </ul>
                    `,
      },
    });
    return plzFeatureLayer;
}


const createFeatureLayer = (data) => {
  // create the layer
  if (featureLayer) {
    mapInstance.value.remove(featureLayer);
    featureLayer.destroy()
  } 
  const plzLayer = plzFeaturePreps(data);
  return plzLayer;
}

const loadData = async () => {
  if (!mapInstance) {
    console.log("Map not yet initialized");
    return;
  }
  // load poins, if present
  if (props.poiUrl) {
    console.log("Fetching POI data from", props.poiUrl);
    const response = await fetch(props.poiUrl);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    poiData.value = await response.json();
    console.log("POI data loaded", poiData);
    if (poiLayer) {
      console.log("Removing POI layer");
      poiLayer.removeAll();
      mapInstance.remove(poiLayer);
      poiLayer = null;
    }
    poiLayer = createPoiLayer(poiData.value)
    mapInstance.add(poiLayer);
  } else {
    console.log("No POI data available");
    poiData.value = null;
  }
  // load features, if present
  if (props.featureUrl) {
    console.log("Fetching Feature data from", props.featureUrl);
    const response = await fetch(props.featureUrl);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    featureData.value = await response.json();
    console.log("Feature data loaded", featureData.value);
    if (featureLayer) {
      console.log("Removing Feature layer");
      mapInstance.remove(featureLayer);
      featureLayer.destroy()
      featureLayer = null;
    }
    featureLayer = createFeatureLayer(featureData.value)
    mapInstance.add(featureLayer);
  } else {
    console.log("No Feature data available");
    featureData.value = null;
  }

  emit("data", { content: [poiData.value, featureData.value], id: theMap.value, view: viewInstance });
};


onMounted(async () => {
  console.log("Map mounted", theMap.value);
  console.log("Props", props);  
  if (!mapInstance) {
    console.log("setupMap");
    mapInstance = new Map();

    // Make map view and bind it to the map
    const view = new MapView({
      container: theMap.value,
      map: mapInstance,
      center: [8.4, 49.01],
      zoom: 13,
      minzoom: 13,
      maxzoom: 18
    });
    viewInstance = view;

    const layerList = new LayerList({
      view: viewInstance
    });

    const llExpand = new Expand({
      view: viewInstance,
      content: layerList,
      expanded: false,
    })
    viewInstance.ui.add(llExpand, "top-right");
    /*
    const legend = new Legend({
      view: view
    });
    view.ui.add(legend, "bottom-right");
    */
    const homeWidget = new Home({
      view: viewInstance
    });

    viewInstance.ui.add(homeWidget, 'top-left')
    viewInstance.ui.add(logoDiv.value, "bottom-right");

    console.log("Loading tiles from ", props.dataUrl);  
    tileLayer = new VectorTileLayer({
      url: props.dataUrl,
      title: "Karlsruhe",
      copyright: "©Stadt Karlsruhe, OK Lab Karlsruhe"
    });
    console.log("tileLayer loaded", tileLayer);
    mapInstance.add(tileLayer);

  }

  await loadData()
});

onUnmounted(async () => {
  console.log("Map unmounted");
  if (viewInstance) {
    console.log("Destroying view");
    viewInstance.destroy();
    viewInstance = null;
    poiLayer = null;
    featureLayer = null;
    mapInstance = null;
  }
});



</script>

<style scoped>
.container {
  height: 100%;
  width: 100%;
  display: flex;
}

.map {
  height: 100%;
  width: 100%;
  padding: 0;
  margin: 0;
  border: unset;
  --calcite-sheet-scrim-background: rgba(0, 0, 0, .1);
}
</style>

<style>

.esri-widget .esrilogo {
  padding: 0.25rem;
  height: 3rem;
  width: auto;
  margin: auto;
}

/* Popup container customization */
.esri-popup {
  font-size: 14px;
  /* Adjust font size for readability */
  max-width: 300px;
  /* Restrict width for smaller screens */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  /* Add rounded corners */
  --calcite-scrim-background: rgba(200, 0, 0, 0.5);
}

/* Popup header styling */
.esri-popup__header {
  background-color: #0079c1;
  color: white;
  font-size: 16px;
  padding: 10px;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

/* Popup content styling */
.esri-popup__content {
  font-size: 14px;
  padding: 10px;
  line-height: 1.5;
}

/* Close button styling */
.esri-popup__button--close {
  color: white;
  font-size: 16px;
}


/* Make the popup fullscreen on mobile (optional) */
@media (max-width: 768px) {
  .esri-popup {
    width: 100%;
    height: auto;
    bottom: 0;
    left: 0;
    right: 0;
    position: fixed;
    border-radius: 0;
  }

  /*
  .esri-expand__panel {
    width: 100%;
    height: auto;
    bottom: 0;
    left: 0;
    right: 0;
    position: fixed;
    border-radius: 0;
  }
*/
  .esri-widget .esrilogo {
    padding: 0.25rem;
    height: 2rem;
  }

}
</style>