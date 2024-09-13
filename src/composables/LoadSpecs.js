// load all specs for a card

const loadHdrMsgs = async(props,langs) => {
    const msgs = await import(`../components/${props.section}/${props.part}/${props.name}/lang.json`) 
  
    for (const key in langs) {
      const lang = langs[key]
      if (msgs[lang].aria === undefined)
        msgs[lang].aria = "Aria " + lang;
    }
    return msgs;
}

const loadHdrText = async(props,langs) => {
    const text = await import(`../components/${props.section}/${props.part}/${props.name}/text.json`); 

    const texts = {}
    for (const key in text) {
      if (langs.includes(key)) texts[key] = text[key];
    }
    return texts;
}

const loadHdrSpecs = async(props) => {
    const specs = await import(`../components/${props.section}/${props.part}/${props.name}/card.json`) 
    const controls = {}
    if (specs.controls) {
      if (specs.controls.range.present) {
        controls.range = specs.controls.range;
        /*
        if (controls.range.step === undefined) {
          controls.range.step = Math.ceil(controls.range.max / 10)
        }
        rangeCtl.value = specs.controls.range.max;
        */
        rangeAxis.value = specs.controls.range.axis || "y";
      }
      else {
        controls.range = false;
      }
      if (specs.controls.dataswitch.present && specs.data.length > 1)
        controls.dataswitch = specs.controls.dataswitch;
      else controls.dataswitch = false;
      if (specs.controls.type) {
        chartType.value = specs.controls.type.options[0];
        if (specs.controls.type.present) controls.type = specs.controls.type;
      } else {
        controls.type = false;
      }
  
      if (specs.controls.stacked.present)
        controls.stacked = specs.controls.stacked;
      else controls.stacked = false;
      if (specs.controls.animate.present)
        controls.animate = specs.controls.animate;
      else controls.animate = false;
    }
    return controls
 
}
  
export { loadHdrMsgs, loadHdrText, loadHdrSpecs }
