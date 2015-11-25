import Ember from 'ember';

import {momentTime} from '../../helpers/moment-time';
import {momentRange} from '../../helpers/moment-range';

export default Ember.Component.extend({

    tagName: 'span',
    start_time: null,
    end_time: null,

    corrected_end_time: function(){
    	return this.get('end_time')?this.get('end_time'):moment().unix();
    }.property('end_time'),
    
    humanized_start_time: function() {
        return momentTime([], {unix: this.get('start_time')});
    }.property('start_time'),  
    
    humanized_range: function() {
        return momentRange([], {start_time: this.get('start_time'),
                                end_time: this.get('corrected_end_time')});
    }.property('start_time', 'corrected_end_time'),
});
