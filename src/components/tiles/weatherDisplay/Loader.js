

const loadKaWeatherData = async (url) => {
    console.log("Loader url:", url)
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data  = await response.json();
    console.log("JSON data:", data);
    const dataItems = {}
    const currentDate = new Date();
    const oneHourAgo = new Date(currentDate.getTime() - 60 * 60 * 1000); // Subtract 1 hour in milliseconds
    const dateValues = []   
    for (const item in data) {
      const dt = new Date(data[item].body[0].measured_at)
      dataItems[item] = data[item];
      // reset value  if older than 1 hour
      if (dt < oneHourAgo) {
          dataItems[item].body[0].data.temperature = undefined
      } else {
          dateValues.push(dt)
      }
    }
    // console.log("Filtered Data:", dataItems);

    const computeMeanDate = (dates) => {
      const sum = dates.reduce((total, date) => total + date.getTime(), 0);
      const meanTime = sum / dates.length;
      const meanDate = new Date(meanTime);
      return meanDate;
    };

    const meanDate = computeMeanDate(dateValues);
    console.log("Mean Date:", meanDate);

    return {"data":dataItems,"date":meanDate};
}

export { loadKaWeatherData };

