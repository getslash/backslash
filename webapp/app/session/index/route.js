import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import RefreshableRouteMixin from '../../mixins/refreshable-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, RefreshableRouteMixin, {

    title: 'Session Details',

    queryParams: {
        humanize_times: {
            refreshModel: false,
        },
        page: {
            refreshModel: true
        },
        filter: {
            refreshModel: true,
        },
        show_successful: {
            refreshModel: true,
        },
        show_unsuccessful: {
            refreshModel: true,
        },
        show_abandoned: {
            refreshModel: true,
        },
        show_skipped: {
            refreshModel: true,
        },
    },


    model: function(params) {
        let session = this.modelFor('session');
        const session_id = parseInt(session.id);

        let query_params = {
                session_id: session_id,
                page: params.page,
                filter: params.filter,
                page_size: 50
        };

        for (let key in params) {
            if (key.startsWith('show_')) {
                query_params[key] = params[key];
            }
        }


        return Ember.RSVP.hash({
            'metadata': this.api.call('get_metadata', {
                entity_type: 'session',
                entity_id: session_id
            }).then(r => r.result),
            'user': this.store.find('user', session.get('user_id')),
            'tests': this.store.query('test', query_params),
            'activity': this.store.query('activity', {session_id: parseInt(session.id)})
        });
    },

    setupController: function(controller, model) {
      this._super(controller, model);
      controller.setProperties(model);
      controller.set('session_model', this.modelFor('session'));
    }

});
