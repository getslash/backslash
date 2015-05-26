import Ember from 'ember';

export default Ember.Route.extend({
    model: function() {
        return {features: [
            {name: "Font Awesome", ok: true},
            {name: "Ember.js", ok: true},
            {name: "Bootstrap", ok: true}
        ]};
    },

  actions: {
    goBack: function () {
      window.history.go(-1);
    },
    showModal: function(name, model) {
      this.render(name, {
        into: 'application',
        outlet: 'modal',
        model: model
      });
    },

    closeModal: function () {
      return this.disconnectOutlet({
        outlet: 'modal',
        parentView: 'application'
      });
    }
  }
});
