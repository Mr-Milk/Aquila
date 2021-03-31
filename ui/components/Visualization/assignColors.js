import { max as maxArr, min as minArr } from "mathjs";

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
