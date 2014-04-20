module.exports = Ember.Route.extend({

    model: function() {

        var self = this;

        var returned = Ember.Object.create({

            features: [
                {name: "Font Awesome", ok: true},
                {name: "Ember.js", ok: true},
                {name: "Bootstrap", ok: true}
            ]
        });

        return returned;
    }

});
