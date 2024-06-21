<template>
  <div class="container">
    <div class="map" ref="theMap"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

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

// Fix Leaflet's default icon paths
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

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

import geojsonData2 from "@/assets/data/ka_geschwindigkeiten_short.json";
import geojsonData3 from "@/assets/data/ka_escooter_short.json";

const geojsonData = ref(geojsonData3);

const theMap = ref(null);

onMounted(() => {
  const map = L.map(theMap.value).setView([49.0069, 8.4037], 13); // Karlsruhe coordinates

  L.tileLayer(
    //'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    "https://tiles-eu.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png",

    {
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
    }
  ).addTo(map);

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
      const features = geojsonData.value.features;
      for (const f of features) {
        console.log("Feature", f);
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
      }
    }
  }

  L.geoJSON(geojsonData.value, {
    onEachFeature: (feature, layer) => {
      if (feature.properties && feature.properties.name) {
        layer.bindPopup(feature.properties.name);
      }
    },
  }).addTo(map);
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
