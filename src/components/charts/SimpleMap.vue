<template>
  <div class="container">
    <div class="map" ref="theMap"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const emit = defineEmits(["data"]);

const props = defineProps({
  /* Add your props here */
  dataUrl: {
    type: String,
    required: true,
  },
  dataName: {
    type: String,
    default: "LineChart",
  },
  ariaLabel: {
    type: String,
    default: "Aria LineChart",
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
    default: { "name": "name", "url": "url", "date":"date",
      "attribution": "attribution", "description": "description" },
  },
  locale: {
    type: String,
    default: "de",
  },
});

//const Lref = ref(L);
const mapInstance = ref(null);
const theMap = ref(null);
const Lref = ref(null);
const tileLayer = ref(null);
const geoLayer = ref(null);

// coordinate conversion
import proj4 from "proj4";
// EPSG is frequently used in Germany
const EPSG25832 = "+proj=utm +zone=32 +ellps=GRS80 +units=m +no_defs";
// EPSG4326 is WGS84, default for Leaflet
const EPSG4326 = "+proj=longlat +datum=WGS84 +no_defs";

// Import Leaflet marker images
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";


const geojsonDataExample = {
  type: "FeatureCollection",
  name: "Testing WGS84",
  crs: {
    type: "name",
    properties: {
      name: "urn:ogc:def:crs:EPSG::4326",
    },
  },
  features: [
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [8.4037, 49.0069], // Karlsruhe
      },
      properties: {
        name: "Marker 1",
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [8.4097, 49.0069], // Nearby Karlsruhe
      },
      properties: {
        name: "Marker 2",
      },
    },
  ],
};


const geojsonData = ref(null);


const tileSource = [
  {
    "name": "osm",
    "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    "attr": "© OpenStreetMap contributors"
  },
  {
    "name": "stadiaOsm",
    "url": "https://tiles-eu.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}@2x.png",
    "attr":
      '\
      &copy; <a href="https://stadiamaps.com/" target="_blank">Stadia Maps</a>|\
      &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a>|\
      &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>\
      '
    //'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>'
  },
  {
    "name": "BaseMapDE",
    "url": "https://sgx.geodatenzentrum.de/wmts_basemapde/tile/1.0.0/de_basemapde_web_raster_farbe/default/GLOBAL_WEBMERCATOR/{z}/{y}/{x}.png",
    "attr": '\
&copy; <a href="https://www.bkg.bund.de" target="_blank">GeoBasis-DE/BKG (' + new Date().getFullYear() + ')</a>|\
<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC BY 4.0</a>\
'
  }

]

const tileIdx = 2 // which tiles to use


watch(() => props.dataUrl, async (newVal, oldVal) => {
  console.log("Data URL changed", newVal, oldVal);
  await loadData();
});

const loadData = async () => {
  console.log("Fetching data from", props.dataUrl);
  const response = await fetch(props.dataUrl);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  geojsonData.value = await response.json();
  // limit number of features
  const features = geojsonData.value.features;
  const maxFeatures = 100;
  if (features.length > maxFeatures) {
    geojsonData.value.features = features.slice(0, maxFeatures);
    console.log(`Only first ${maxFeatures} features are loaded.`)
  }

  // check crs: if not WGS84, transform to WGS84
  const crs = geojsonData.value.crs;
  console.log("CRS:", crs);
  if (crs && crs.properties) {
    const crsName = crs.properties.name;
    console.log("CRS:", crsName, crs);
    if (
      crsName &&
      crsName.toLowerCase().includes("epsg") &&
      crsName.includes("25832")
    ) {
      console.log("Transforming from", crsName);
      // make sure to update crs else will be transformed again on reload
      crs.properties.name = "WGS84"
      const features = geojsonData.value.features;

      for (const f of features) {
        //console.log("Feature", f);
        const geom = f.geometry;
        if (geom.type.toLowerCase() == "point") {
          const coords = geom.coordinates;
          const transformed = proj4(EPSG25832, EPSG4326, coords);
          geom.coordinates = transformed;
        }
        if (geom.type.toLowerCase() == "linestring") {
          const coords = geom.coordinates;
          for (let i = 0; i < coords.length; i++) {
            const transformed = proj4(EPSG25832, EPSG4326, coords[i]);
            coords[i] = transformed;
          }
        }
        if (geom.type.toLowerCase() == "polygon") {
          const coords = geom.coordinates;
          for (let j = 0; j < coords.length; j++) {
            for (let i = 0; i < coords[j].length; i++) {
              const transformed = proj4(EPSG25832, EPSG4326, coords[j][i]);
              coords[j][i] = transformed;
            }
          }
        }
      }
    }
  }

  if (geoLayer.value)
    await geoLayer.value.removeFrom(mapInstance.value)

  geoLayer.value = Lref.value.geoJSON(geojsonData.value, {
    onEachFeature: (feature, layer) => {
      if (feature.properties && feature.properties[props.dataProps.name]) {
        // layer.bindPopup(feature.properties.name);
        let popupContent = "<b>" + feature.properties[props.dataProps.name] + "</b><br>"
        if (feature.properties[props.dataProps.description])
          popupContent += feature.properties[props.dataProps.description] + "<br>"
        if (feature.properties[props.dataProps.date])
          popupContent += "Date: " + feature.properties[props.dataProps.date] + "<br>"
        if (feature.properties[props.dataProps.img])
          popupContent +=
            "<img src='" + feature.properties[props.dataProps.img] + "' width='160'><br>" +
            "<em>" + feature.properties[props.dataProps.attribution] + "</em><br>"
        if (feature.properties[props.dataProps.url])
          popupContent += "<a href='" + feature.properties[props.dataProps.url] + "' target=_blank>More</a><br>"
        layer.bindPopup(popupContent);
      }
    },
  })
  geoLayer.value.addTo(mapInstance.value);
  emit("data", { content: geojsonData.value, id: theMap.value, L: Lref.value, map: mapInstance.value });
};


onMounted(async () => {
  console.log("Map mounted")
  console.log("Props", props);
  if (!mapInstance.value) {
    Lref.value = L;
    // Fix Leaflet's default icon paths
    delete Lref.value.Icon.Default.prototype._getIconUrl;

    Lref.value.Icon.Default.mergeOptions({
      iconRetinaUrl: markerIcon2x,
      iconUrl: markerIcon,
      shadowUrl: markerShadow,
    });

    mapInstance.value = Lref.value.map(theMap.value).setView([49.0069, 8.4037], 13); // Karlsruhe coordinates
  }

  tileLayer.value = Lref.value.tileLayer(
    tileSource[tileIdx].url,
    {
      maxZoom: 19,
      attribution: tileSource[tileIdx].attr,
    }
  )
  tileLayer.value.addTo(mapInstance.value);
  // load geojson ...
  await loadData()
});

onUnmounted(async () => {
  console.log("Map unmounted");
  await geoLayer.value.clearLayers();
  await tileLayer.value.removeFrom(mapInstance.value)
  await geoLayer.value.removeFrom(mapInstance.value)
  // await mapInstance.value.remove();
  mapInstance.value = null;
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
}
</style>
