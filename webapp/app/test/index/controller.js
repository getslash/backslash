import Ember from 'ember';
/* global moment */

export default Ember.Controller.extend({

    is_method: Ember.computed.notEmpty('info.class_name'),

    duration_string: function() {
        let t = moment.unix(this.get('test.start_time')).twix(moment.unix(this.get('test.end_time')));
        return t.humanizeLength();
    }.property('test.start_time', 'test.end_time'),

    is_ended: Ember.computed.notEmpty('test.end_time'),


    scm_details: function() {
        let self = this;
        let test = self.get('test');

        if (!test.get('scm')) {
            return {};
        }

        return Ember.Object.create({
            'Revision': test.get('scm_revision'),
            'File Hash': test.get('file_hash')
        });

    }.property('test'),

});
