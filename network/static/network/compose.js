const TWEET_CHARACTER_LIMIT = 140;

document.addEventListener('DOMContentLoaded', () => {
  const color = 'rgb(255, 255, 255)';
  // set a change eventlistener for the input box
  if (document.querySelector('#compose-form-post-text')) {
    document.querySelector('#compose-form-post-text').addEventListener('keyup', updatePostCharCounter);
  }
  console.log("compose.js loaded");
});

function updatePostCharCounter() {
  let postLength = document.querySelector('#compose-form-post-text').value.length;
  const startingColor = getComputedStyle(document.querySelector('#compose-form-post-text')).backgroundColor;
  const endColor = getComputedStyle(document.querySelector('#compose-form-character-count-end-color')).color;
  let currentColor = calculateInBetweenColor(startingColor, endColor, postLength, TWEET_CHARACTER_LIMIT);
  document.querySelector('#compose-form-character-count').innerHTML = `${postLength}/${TWEET_CHARACTER_LIMIT}`;
  document.querySelector('#compose-form-character-count').style.color = currentColor;
}

function calculateInBetweenColor(rgbColor1, rgbColor2, step, numSteps) {
  // Calculates the color between two colors, given a step and number of steps
  // INPUTS:
  //   2 strings in the format "rbg(a, b, c)"
  //   the step between the two colors
  //   the number of steps
  // OUTPUT:
  //   a string in the format "rbg(a, b, c)"
  //        which represents the color between the two colors
  //        at the given step and number of steps
  //   e.g. calculateInBetweenColor("rbg(255, 0, 0)", "rbg(0, 255, 0)", 70, 140)
  //        would return "rgb(128, 128, 0)"

  // split the two colors into an array of r, g, b
  const [r1, g1, b1] = rgbColor1.slice(4, -1).split(',').map(x => parseInt(x));
  const [r2, g2, b2] = rgbColor2.slice(4, -1).split(',').map(x => parseInt(x));
  // calculate the step between the two colors
  const stepR = (r2 - r1) / numSteps;
  const stepG = (g2 - g1) / numSteps;
  const stepB = (b2 - b1) / numSteps;
  // calculate the color at each step
  const colorR = r1 + stepR * step;
  const colorG = g1 + stepG * step;
  const colorB = b1 + stepB * step;
  // return the color as a string in the format "rbg(a, b, c)"
  return `rgb(${colorR}, ${colorG}, ${colorB})`;
}
