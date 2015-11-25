import Ember from 'ember';
import BaseController from '../controllers/base';
import config from '../config/environment';

export default BaseController.extend({

    session: Ember.inject.service(),

    path_tracker: Ember.inject.service(),

    app_version: config.app_version,

    _path_observer: function() {
        this.get('path_tracker').set('path', this.get('currentPath'));
    }.observes('currentPath'),

    actions: {
        invalidateSession: function() {
            this.get('session').invalidate();
        }
    }
});
