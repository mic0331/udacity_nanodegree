'use strict';

var express = require('express'),
    controller = require('./eurostat.controller');

var router = express.Router();

router.get('/', controller.index);
router.get('/country/:id', controller.getByCountry);
router.get('/basic/country/:id', controller.getNETforA1_50_all)

module.exports = router;