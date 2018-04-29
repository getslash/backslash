import Component from '@ember/component';

export default Component.extend({
  classNames: ["container-fluid"],

  side: { side: true, main: false },
  main: { side: false, main: true },

  collapsed: false
});
