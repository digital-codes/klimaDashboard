<template>
  <div class="container">
    <div class="map" ref="theMap"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const emit = defineEmits(["data"]);

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


const geojsonData1 = {
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

//import geojsonData2 from "@/assets/data/ka_geschwindigkeiten.json";
//import geojsonData3 from "@/assets/data/ka_escooter.json";
//import geojsonData4 from "@/assets/data/ka_stadtteile.json";
import geojsonData_ from "@/assets/data/weatherPois.json";


const geojsonData = ref(geojsonData_);


const tileSource = [
  {
    "name": "osm",
    "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    "attr": "© OpenStreetMap contributors"
  },
  {
    "name": "stadiaOsm",
    "url": "https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}@2x.png",
    "attr": '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>'
  }
]

const tileIdx = 1 // which tiles to use

onMounted(() => {
  console.log("Map mounted")
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

  geoLayer.value = Lref.value.geoJSON(geojsonData.value, {
    onEachFeature: (feature, layer) => {
      if (feature.properties && feature.properties.name) {
        // layer.bindPopup(feature.properties.name);
        var popupContent = "<b>" + feature.properties.name + "</b><br>" +
                    "<img src='" + feature.properties.url + "' width='200'><br>" +
                    "<em>" + feature.properties.attribution + "</em><br>"
                
                layer.bindPopup(popupContent);        
      }
    },
  })
  geoLayer.value.addTo(mapInstance.value);
  emit("data", { content: geojsonData.value, id: theMap.value, L: Lref.value, map: mapInstance.value });
});

onUnmounted(async () => {
  console.log("Map unmounted");
  await geoLayer.value.clearLayers();
  await geoLayer.value.removeFrom(mapInstance.value)
  await tileLayer.value.removeFrom(mapInstance.value)
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
