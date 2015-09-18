import BaseController from '../controllers/base';

export default BaseController.extend({

    app_controller: Ember.inject.controller('application'),

    current_path: Ember.computed.oneWay('app_controller.currentPath')
});
