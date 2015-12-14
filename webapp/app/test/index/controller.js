import Ember from 'ember';
import {momentTime} from '../../helpers/moment-time';

/* global moment */

export default Ember.Controller.extend({

    is_method: Ember.computed.notEmpty('info.class_name'),

    test_details: function() {
        let self = this;
        let test = self.get('test');

        let returned = Ember.Object.create({
            'File name': test.get('info.file_name'),
        });
        returned.set(self.get('is_method')?'Method':'Function', test.get('info.name'));

        if (test.get('end_time')) {
        	let end_time = test.get('end_time')?moment.unix(test.get('end_time')):moment.unix();
        	let time_range = moment.unix(test.get('start_time')).twix(end_time);
        	returned.set('Run time', time_range.simpleFormat('YYYY/MM/DD HH:mm:ss'));
        	returned.set('Duration', time_range.humanizeLength());
        } else {
        	returned.set('Run time', 'Started ' + momentTime([], {ago:test.get('start_time')}));
        }

        if (self.get('test.is_skipped')) {
            returned.set('Skip Reason', self.get('test.skip_reason'));
        }

        return returned;

    }.property('test'),


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
