/**
 * Using Rails-like standard naming convention for endpoints.
 * GET     /eurostat            ->  index
 */

'use strict';

var Eurostat  = require('./eurostat.model');

function handleError(res, err) {
    return res.status(500).json(err);
}

// Get everything.
exports.index = function(req, res) {
    Eurostat.find({}).exec(function(err, collection) {
        if(err) { return handleError(res, err); }
        return res.status(200).json(collection);
    })
};

// Get a single country.
exports.getByCountry = function(req, res) {
    Eurostat.find({'country.code': req.params.id}, function (err, data) {
        if(err) { return handleError(res, err); }
        if(!data) { return res.status(404).end(); }
        return res.json(data).end();
    });
};

exports.getNETforA1_50_all = function(req, res) {
    Eurostat.find({
        'ecase.code': "A1_50", // "Single person without children, 100% of AW"
        'currency.code': "EUR",
        'country.code': req.params.id
    })
    .sort({'measure.year' :  -1})
    .select('measure estruct')
    .exec(function (err, data) {
        if(err) { return handleError(res, err); }
        if(!data) { return res.status(404).end(); }
        return res.json(data).end();
    });
};