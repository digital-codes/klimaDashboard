<template>
<div class="container">
  <div class="map" ref="theMap" ></div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Import Leaflet marker images
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// Fix Leaflet's default icon paths
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});


const geojsonData = {
type: 'FeatureCollection',
features: [
    {
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: [8.4037, 49.0069], // Karlsruhe
    },
    properties: {
        name: 'Marker 1',
    },
    },
    {
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: [8.4097, 49.0069], // Nearby Karlsruhe
    },
    properties: {
        name: 'Marker 2',
    },
    },
],
};

const theMap = ref(null)

onMounted(() => {
    const map = L.map(theMap.value).setView([49.0069, 8.4037], 13); // Karlsruhe coordinates

    L.tileLayer(
        //'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
        "https://tiles-eu.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png",

    {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
    }).addTo(map);


    L.geoJSON(geojsonData, {
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
  display:flex;
}
.map {
  height: 100%;
  width: 100%;
}
</style>
