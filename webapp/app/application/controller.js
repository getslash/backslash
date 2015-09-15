import Ember from 'ember';
import BaseController from '../controllers/base';

export default BaseController.extend({

    session: Ember.inject.service()
});
