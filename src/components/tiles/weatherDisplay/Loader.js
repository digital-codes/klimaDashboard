

const loadKaWeatherData = async (url) => {
    console.log("Loader url:", url)
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data  = await response.json();
    console.log("JSON data:", data);
    return data
}

export { loadKaWeatherData };

