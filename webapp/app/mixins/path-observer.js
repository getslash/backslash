import Ember from 'ember';

export default Ember.Mixin.create({

    app_controller: Ember.inject.controller('application'),

    current_path: Ember.computed.oneWay('app_controller.currentPath')

});
