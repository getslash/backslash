
import Ember from 'ember';
var Promise = Ember.RSVP.Promise;

export default function preloadImages(...urls) {
  let promises = urls.map(url => {
    return new Promise((resolve, reject) => {
      let image = new Image();
      image.onload = resolve;
      image.onerror = reject;
      image.src = url;
    });
  });

  return Promise.all(promises);
}


export function initialize(/* application */) {
    const images = ["backslash-fire.jpg"];

    for (let img of images) {
        let image = new Image();
        image.src = "/static/img/" + img;
    }
}

export default {
  name: 'image-preloads',
  initialize
};
