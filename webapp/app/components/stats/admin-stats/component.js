import Ember from 'ember';

/* global d3 */

export default Ember.Component.extend({

    data: null,
    series_key: null,
    series_name: null,
    floating_point: false,

    formatter: function(v) {
        return d3.format(this.get('floating_point')?'g':'d')(v);
    },

    _data: function() {
        let returned = {
            json: this.get('data'),
            type: 'area-spline',
            keys: {
                x: 'timestamp',
                value: [this.get('series_key')],
            },

            names: {},
        };
        returned.names[this.get('series_key')] = this.get('series_name');
        return returned;
    }.property(),

    _axis: function() {
        return {
            y: {
                min: 0,
                padding: {
                    bottom: 0,
                },
                tick: {
                    format: this.get('formatter').bind(this),
                },
            },
            x: {
                type: 'timeseries',
                tick: {
                    culling: {
                        max: 3,
                    },
                    format(x) {
                        return moment.unix(x).format('L LTS');
                    }
                }
            }
        };
    }.property(),
});
