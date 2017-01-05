import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import LoadingIndicatingRoute from '../mixins/loading-indicating-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, LoadingIndicatingRoute, {

    titleToken: 'Subjects',

    queryParams: {
        page: {
            refreshModel: true,
        },
        page_size: {
            refreshModel: true,
        },
        sort: {
            refreshModel: true,
        },
    },

    model(params) {
	let sort_order = params.sort;

        return Ember.RSVP.hash({
            subjects: this.store.query('subject', {page: params.page, page_size: params.page_size, sort: sort_order}),
        });
    },

    setupController(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
        controller.set('page', model.subjects.get('meta.page'));
    },
});
