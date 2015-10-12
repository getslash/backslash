import Ember from 'ember';

var api = {
    call: function(name, params) {
        return Ember.$.ajax({
            type: 'POST',
            url: '/api/' + name,
            contentType: 'application/json',
            data: JSON.stringify(params)
        });
    }
};


export function initialize(application) {
    application.register('api:main', api, {instantiate: false});

    application.inject('controller', 'api', 'api:main');
    application.inject('route', 'api', 'api:main');
}

export default {
  name: 'api',
  initialize: initialize
};
