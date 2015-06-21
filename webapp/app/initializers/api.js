import Ember from 'ember';

var api = {
    call: function(params) {
        return Ember.$.ajax({
            type: 'POST',
            url: '/api/get_metadata',
            contentType: 'application/json',
            data: JSON.stringify(params)
        });
    }
};


export function initialize(container, application) {
    application.register('api:main', api, {instantiate: false});

    application.inject('controller', 'api', 'api:main');
    application.inject('route', 'api', 'api:main');
}

export default {
  name: 'api',
  initialize: initialize
};
