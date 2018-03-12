import Component from '@ember/component';

export default Component.extend({

  actions: {
    back: function() {
      window.history.back();
    }
  }
});
