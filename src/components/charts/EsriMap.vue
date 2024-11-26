<template>
  <div class="container">
    <div class="map" ref="theMap"></div>
    <div ref="logoDiv" class="logo">
      <img src="/icons/favicon.svg" alt="Logo" />
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


const emit = defineEmits(["data"]);

const props = defineProps({
  /* Add your props here */
  dataUrl: {
    // basemap url
    type: String,
    //required: true,
    default: "https://geoportal.karlsruhe.de/ags04/rest/services/Hosted/Regiokarte_farbig_reduziert/VectorTileServer"
  },
  poiUrl: {
    type: String | null,
    default: "/data/karlsruhe/weatherPois.json",
  },
  featureUrl: {
    type: String | null,
    default: "/data/karlsruhe/plz.geojson"
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

//const Lref = ref(L);
const mapInstance = ref(null);
const viewInstance = ref(null);
const logoDiv = ref(null);
const theMap = ref(null);


const tileLayer = ref(null); // map tiles
const featureLayer = ref(null); // geojson layer for features
const poiLayer = ref(null); // point of interest layer, geojson
const featureData = ref(null); // geojson layer for features
const poiData = ref(null); // point of interest layer, geojson



watch(() => props.dataUrl, async (newVal, oldVal) => {
  console.log("Data URL changed", newVal, oldVal);
  await loadData();
});
watch(() => props.poiUrl, async (newVal, oldVal) => {
  console.log("POI URL changed", newVal, oldVal);
  await loadData();
});
watch(() => props.featureUrl, async (newVal, oldVal) => {
  console.log("Feature URL changed", newVal, oldVal);
  await loadData();
});

const addPoi = (longitude, latitude, title, content) => {
  var point = {
    type: "point", // autocasts as new Point()
    longitude: longitude,
    latitude: latitude
  };
  var markerSymbol = new PictureMarkerSymbol({
    url: "assets/custom/icons/marker-icon-2x.png",  // Path to your custom icon
    width: "32px", // Adjust size as needed
    height: "50px",
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
  if (poiLayer.value)
    poiLayer.value.removeAll();
  else {
    poiLayer.value = new GraphicsLayer();
    mapInstance.value.add(poiLayer.value);
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
    poiLayer.value.add(poi);
  });
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
      /*
      renderer: {
        type: "simple", // Simple renderer
        symbol: {
          type: "simple-fill",
          color: [0, 0, 0, 0.2], // Fill color with transparency
          outline: {
            color: [255, 255, 255],
            width: 1,
          },
        },
      },
      */
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
  if (featureLayer.value) {
    featureLayer.value.removeAll();
    mapInstance.value.remove(featureLayer.value);
  } 
  const plzLayer = plzFeaturePreps(data);
  mapInstance.value.add(plzLayer);
}

const loadData = async () => {
  if (!mapInstance.value) {
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
    console.log("POI data loaded", poiData.value);
    if (poiLayer.value) {
      console.log("Removing POI layer");
      poiLayer.value.removeAll();
      mapInstance.value.remove(poiLayer.value);
      poiLayer.value = null;
    }
    poiLayer.value = createPoiLayer(poiData.value)
    mapInstance.value.add(poiLayer.value);
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
    if (featureLayer.value) {
      console.log("Removing Feature layer");
      featureLayer.value.removeAll();
      mapInstance.value.remove(featureLayer.value);
      featureLayer.value = null;
    }
    featureLayer.value = createFeatureLayer(featureData.value)
    mapInstance.value.add(featureLayer.value);
  } else {
    console.log("No Feature data available");
    featureData.value = null;
  }

  emit("data", { content: [poiData.value, featureData.value], id: theMap.value, view: viewInstance.value });
};


onMounted(async () => {
  console.log("Map mounted", theMap.value);
  if (!mapInstance.value) {
    console.log("setupMap", element);
    const map = new Map();
    mapInstance.value = map;

    // Make map view and bind it to the map
    const view = new MapView({
      container: theMap.value.id,
      map: map,
      center: [8.4, 49.01],
      zoom: 13,
      minzoom: 13,
      maxzoom: 18
    });
    viewInstance.value = view;

    const layerList = new LayerList({
      view: view
    });
    //view.ui.add(layerList, "top-right");
    const llExpand = new Expand({
      view: view,
      content: layerList,
      expanded: false
    })
    view.ui.add(llExpand, "top-right");
    /*
    const legend = new Legend({
      view: view
    });
    view.ui.add(legend, "bottom-right");
    */
    const homeWidget = new Home({
      view: view
    });

    view.ui.add(homeWidget, 'top-left')
    console.log("Logodiv", logoDiv.value);
    view.ui.add(logoDiv.value.id, "bottom-right");

    const tiles = new VectorTileLayer({
      url: props.dataUrl,
      title: "Karlsruhe",
      copyright: "©Stadt Karlsruhe, OK Lab Karlsruhe"
    });
    console.log("tileLayer loaded", tiles);
    tileLayer.value = tiles;
    map.add(tiles);

  }

  await loadData()
});

onUnmounted(async () => {
  console.log("Map unmounted");
  if (viewInstance.value) {
    console.log("Destroying view");
    viewInstance.value.destroy();
    viewInstance.value = null;
    poiLayer.value = null;
    featureLayer.value = null;
    mapInstance.value = null;
  }
});



</script>

<style scoped>
.container {
  height: 100%;
  width: 100%;
  position: relative;
  display: flex;
}

.map {
  height: 100%;
  width: 100%;
  padding: 0;
  margin: 0;
  --calcite-sheet-scrim-background: rgba(0, 0, 0, .1);
}
</style>

<style>
/*
.map {
  padding: 0;
  margin: 0;
  height: 60vh;
  width: 80vw;
  border:solid 1px blue;
  --calcite-sheet-scrim-background: rgba(0, 0, 0, .1);
}
*/
.esri-widget .logo {
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

  .esri-widget .logo {
    padding: 0.25rem;
    height: 2rem;
  }

}
</style>