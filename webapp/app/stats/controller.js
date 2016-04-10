import Ember from 'ember';

export default Ember.Controller.extend({

    session: Ember.inject.service(),

    load_avg_gauge_data: function() {
        return {
            columns:  [
                ['load', this.get('model.current.stat_system_load_avg')],
            ],
            type: 'gauge',
        };
    }.property('model'),

    load_avg_gauge_settings: function() {
        return {
            min: 0,
            max: this.get('model.cpu_count'),
            units: '',
            label: {
                show: false,
                format(avg) {
                    return avg.toFixed(2);
                }
            },
        };
    }.property('model'),

    load_avg_gauge_color: function() {
        let max = this.get('load_avg_gauge_settings.max');
        return {
            pattern: ['green', 'orange', 'red'], // the three color levels for the percentage values.
            unit: 'value',
            threshold: {
                values: [max * 0.5, max * 0.8]
            }
        };
    }.property('model'),


    format_bytes(bytes) {
        if (bytes >= 1000000000) {
            bytes = (bytes / 1000000000).toFixed(2) + ' GB';
        } else if (bytes >= 1000000) {
            bytes = (bytes / 1000000).toFixed(2) + ' MB';
        } else if (bytes >= 1000) {
            bytes = (bytes / 1000).toFixed(2) + ' KB';
        } else if (bytes > 1) {
            bytes = bytes + ' bytes';
        } else if (bytes === 1) {
            bytes = bytes + ' byte';
        } else {
            bytes = '0 byte';
        }
        return bytes;
    }
});
