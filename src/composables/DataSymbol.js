
import { useConfigStore } from '@/services/configStore';
const configStore = useConfigStore();


const getDataSymbol = (index, lib = 'echarts') => {
    let sym
    const isDark = configStore.getTheme == "dark"
    const col = index % 2 ? (isDark ? 'rgb(31,51,153)' : 'rgb(41,68,205)') : (isDark ? 'rgb(228,193,23)' : 'rgb(177,150,18)')
    let pattern
    // pattern is for bar charts, symbols is for line charts, basically
    // The overall rotation angle (in radians) of the pattern
    switch (index) {
        case 0:
        case 1:
            sym = 'circle'
            pattern = Math.PI / 4
            break;
        case 2:
        case 3:
            sym = lib == "echarts" ? 'diamond' : 'rectRot'
            pattern = -Math.PI / 4
            break;
        case 4:
        case 5:
            sym = 'triangle'
            pattern = Math.PI / 8
            break;
        case 6:
        case 7:
            sym = lib == "echarts" ? 'rectangle' : "rect"
            pattern = -Math.PI / 8
            break;
        default:
            console.error("Unknown index:", index)
            break;
    }
    return { symbol: sym, color: col, pattern: pattern }
}

export default getDataSymbol

/*
chartjs:
    'circle'
    'cross'
    'crossRot'
    'dash'
    'line'
    'rect'
    'rectRounded'
    'rectRot'
    'star'
    'triangle'
    false

*/