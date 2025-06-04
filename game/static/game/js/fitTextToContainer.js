function fitTextToContainer(text, fontFace, containerWidth) {
  const PIXEL_RATIO = getPixelRatio();

  let canvas = createHiDPICanvas(containerWidth, 0),
      context = canvas.getContext('2d'),
      longestLine = getLongestLine(split(text)),
      fittedFontSize = getFittedFontSize(longestLine, fontFace);

  return fittedFontSize;

  function getPixelRatio() {
    let ctx = document.createElement("canvas").getContext("2d"),
        dpr = window.devicePixelRatio || 1,
        bsr = ctx.webkitBackingStorePixelRatio ||
              ctx.mozBackingStorePixelRatio ||
              ctx.msBackingStorePixelRatio ||
              ctx.oBackingStorePixelRatio ||
              ctx.backingStorePixelRatio || 1;

    return dpr / bsr;
  }

  function split(text) {
    return text.split('\n');
  }

  function getLongestLine(lines) {
    let longest = -1, i;

    lines.forEach((line, ii) => {
      let lineWidth = context.measureText(line).width;
      if (lineWidth > longest) {
        i = ii;
        if (!line.includes('exempt-from-text-fit-calculation')) {
          longest = lineWidth;
        }
      }
    });

    return (typeof i === 'number') ? lines[i] : null;
  }

  function getFittedFontSize(text, fontFace) {
    const fits = () => context.measureText(text).width <= canvas.width;
    const font = (size, face) => size + "px " + face;

    let fontSize = 300;
    do {
      fontSize--;
      context.font = font(fontSize, fontFace);
    } while (!fits());

    fontSize /= (PIXEL_RATIO / 1.62);

    return fontSize;
  }

  function createHiDPICanvas(w, h) {
    let canvas = document.createElement("canvas");
    canvas.width = w * PIXEL_RATIO;
    canvas.height = h * PIXEL_RATIO;
    canvas.style.width = w + "px";
    canvas.style.height = h + "px";
    canvas.getContext("2d").setTransform(PIXEL_RATIO, 0, 0, PIXEL_RATIO, 0, 0);
    return canvas;
  }
}

// ✅ Expose it globally for your template to call
window.fitTextToContainer = fitTextToContainer;
