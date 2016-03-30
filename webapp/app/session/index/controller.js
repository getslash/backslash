import Ember from 'ember';
import PaginatedFilteredController from '../../controllers/paginated_filtered_controller';

export default PaginatedFilteredController.extend({

    queryParams: ['humanize_times', 'show_successful', 'show_unsuccessful', 'show_abandoned', 'show_skipped'],

    humanize_times: true,
    show_successful: true,
    show_unsuccessful: true,
    show_abandoned: true,
    show_skipped: true,



    investigating: false,

    collection: Ember.computed.oneWay('tests'),

    needs_investigation: function() {
        return this.get('session_model.investigated') !== true && this.get('session_model.status') !== 'SUCCESS';
    }.property('session_model.investigated', 'session_model.status'),

    toggle: function(attr) {
        let self = this;
        self.api.call('toggle_' + attr, {session_id: parseInt(self.get('session_model.id'))}).then(function() {
            self.set('session_model.' + attr, !self.get('session_model.' + attr));
        }).then(function() {
            self.send('refreshRoute');
        });
    },

    additional_metadata: function() {
        return {'Ran from': this.get('session_model.hostname')};
    }.property('session_model.hostname'),

    actions: {

        start_investigating: function() {
            this.set('investigating', true);
        },

        cancel_investigating: function() {
            this.set('investigating', false);
        },

        finish_investigating: function() {
            let self = this;
            const sid = parseInt(self.get('session_model.id'));

            self.api.call('post_comment', {
                comment: self.get('investigate_conclusion'),
                session_id: sid
            }).then(function() {
                self.api.call('toggle_investigated', {
                    session_id: sid
                }).then(function() {
                    self.set('investigating', false);
                    self.set('session_model.investigated', true);
                    self.send('refreshRoute');
                });
            });
        },

        toggle_archive: function() {
            this.toggle('archived');
        },

        toggle_investigated: function() {
            this.toggle('investigated');
        }
    }
});
