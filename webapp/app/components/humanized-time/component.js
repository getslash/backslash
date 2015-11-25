import Ember from 'ember';

import {momentTime} from '../../helpers/moment-time';
import {momentRange} from '../../helpers/moment-range';

export default Ember.Component.extend({

    tagName: 'span',

    start_time: null,

    humanized_start_time: function() {
        return momentTime([], {unix: this.get('start_time')});
    }.property('start_time'),

    end_time: null,

    humanized_range: function() {
        return momentRange([], {start_time: this.get('start_time'),
                                end_time: this.get('end_time')});
    }.property('start_time', 'end_time'),

    
    is_running: false,

});
