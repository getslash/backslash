import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import LoadingIndicatingRoute from '../mixins/loading-indicating-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, LoadingIndicatingRoute, {

    titleToken: 'Users',

    queryParams: {
        page: {refreshModel: true},
        page_size: {refreshModel: true},
        sort: {
            refreshModel: true,
        },
    },

    model(params) {
	let sort_order = params.sort;

        return Ember.RSVP.hash({
            users: this.store.query('user', {page_size: params.page_size, page: params.page, sort: sort_order}),
        });
    },

    setupController(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
        controller.setProperties({
            page_size: model.users.get('meta.page_size'),
            page: model.users.get('meta.page'),
        });
    },
});
