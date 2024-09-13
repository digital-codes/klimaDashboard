// load all specs for a card

const loadMsgs = async (props, langs, type = "card") => {
  let data = null
  switch (type) {
    case "card":
      data = await import(`../components/tiles/${props.section}/${props.part}/${props.name}/lang.json`)
      break
    case "hdr":
      data = await import(`../components/header/configs/${props.name}/lang.json`)
      break;
    default:
      alert("loadMsgs: unknown type " + type)
      return null
  }

  for (const key in langs) {
    const lang = langs[key]
    if (data[lang].aria === undefined)
      data[lang].aria = "Aria " + lang;
  }
  return data;
}

const loadText = async (props, langs, type = "card") => {
  let data = null
  switch (type) {
    case "card":
      data = await import(`../components/tiles/${props.section}/${props.part}/${props.name}/text.json`)
      break
    case "hdr":
      data = await import(`../components/header/configs/${props.name}/text.json`)
      break;
    default:
      alert("loadText: unknown type " + type)
      return null
  }

  const texts = {}
  for (const key in data) {
    if (langs.includes(key)) texts[key] = data[key];
  }
  return texts;
}

const loadSpecs = async (props, type = "card") => {
  let data = null
  switch (type) {
    case "card":
      data = await import(`../components/tiles/${props.section}/${props.part}/${props.name}/card.json`)
      const controls = {}
      if (data.controls) {
        if (data.controls.range.present) {
          controls.range = data.controls.range;
          /*
          if (controls.range.step === undefined) {
            controls.range.step = Math.ceil(controls.range.max / 10)
          }
          rangeCtl.value = data.controls.range.max;
          */
          rangeAxis.value = data.controls.range.axis || "y";
        }
        else {
          controls.range = false;
        }
        if (data.controls.dataswitch.present && data.data.length > 1)
          controls.dataswitch = data.controls.dataswitch;
        else controls.dataswitch = false;
        if (data.controls.type) {
          chartType.value = data.controls.type.options[0];
          if (data.controls.type.present) controls.type = data.controls.type;
        } else {
          controls.type = false;
        }

        if (data.controls.stacked.present)
          controls.stacked = data.controls.stacked;
        else controls.stacked = false;
        if (data.controls.animate.present)
          controls.animate = data.controls.animate;
        else controls.animate = false;
      }
      return controls
      break
    case "hdr":
      data = await import(`../components/header/configs/${props.name}/card.json`)
      return data
      break;
    default:
      alert("loadSpecs: unknown type " + type)
      return null
  }

}

export { loadMsgs, loadText, loadSpecs }
