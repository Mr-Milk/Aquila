import {max as maxArr, min as minArr} from "mathjs";

export let palette = [
    '#5470c6',
    '#91cc75',
    '#fac858',
    '#ee6666',
    '#73c0de',
    '#3ba272',
    '#fc8452',
    '#9a60b4',
    '#ea7ccc',
    '#2624c7',
    '#915b1d',
    '#962b00',
    '#06bca4',
    '#a81ad8',
    '#c0c6d3',
    '#3d3d3d',
    '#52325d',
    '#0099cc',
    '#ff4e00',
    '#034c36',
    '#ff2d37',
    '#a80030',
]

export default function assignColor(colors, arr, min = null, max = null) {
    const cut = colors.length;
    let min_v, max_v;

    if (min === null) {
        max_v = maxArr(arr);
        min_v = minArr(arr);
    } else {
        max_v = max;
        min_v = min;
    }

    const range = max_v - min_v;

    const bin = range / cut;

    let ranges = {};
    let start = min_v;
    colors.map((c) => {
        ranges[c] = [start, start + bin];
        start += bin;
    });

    return arr.map((a) => {
        if (a === max_v) {
            return colors.slice(-1)[0];
        } else {
            for (let i = 0; i < cut; i++) {
                let c = colors[i];
                let r = ranges[c];
                if (a >= r[0] && a < r[1]) {
                    return c;
                }
            }
        }
    });
}
