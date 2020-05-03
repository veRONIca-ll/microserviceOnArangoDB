function to_right_register(city_name){
	return city_name.slice(0,1).toUpperCase() + city_name.slice(1,city_name.length)
}



'use strict';
const createRouter = require('@arangodb/foxx/router');
const router = createRouter();

module.context.use(router);
const arangodb = require("@arangodb");
const db = arangodb.db;
const aql = arangodb.aql;

const err_city = {"code": 0, "message": "No such city in db"};
const err_way = {"code": 1, "message": "Edge was not found"};


var joi = require("joi");
// const cityCollection = db._collection('cities');

router.get('/time/:cityFrom/:cityTo/:amountOfPaths', function (req, res) {

	var city_from = req.pathParams.cityFrom;
	var city_to = req.pathParams.cityTo;
	var paths = req.pathParams.amountOfPaths
    
	var city_from_key = db._query(aql`for city in cities filter city.name == ${to_right_register(city_from)} return city._key`).next();
	var city_to_key = db._query(aql`for city in cities filter city.name == ${to_right_register(city_to)} return city._key`).next();

    if (city_to_key == null || city_from_key == null) res.throw(err_city);

	var aql_req = aql`FOR p IN any K_SHORTEST_PATHS concat('cities/', ${city_from_key}) TO concat('cities/', ${city_to_key})
					  GRAPH 'roads'
					  OPTIONS {
					      weightAttribute: 'time',
					      defaultWeight: 0
					          }
					      LIMIT ${Number(paths)}
					      RETURN {
					          places: p.vertices[*].name,
					          travel_time: p.edges[*].time,
					          travel_time_total: CONCAT('~ ', ROUND(SUM(p.edges[*].time)/60), ' hours')
					      }`
	
		
		const answer = db._query(aql_req);
    	
    	if (answer['_documents'].length == 0){
    		res.send(err_way);
    	}else{
    		res.send(answer);
		}
})
.response(joi.array().items(
    joi.string().required()
).required(), 'List of entry keys.')
.summary('Returns a few shortest path between cities with time.')
.description('Returns a few shortest path between cities with time.');



router.get('/distance/:cityFrom/:cityTo/:amountOfPaths', function (req, res) {

	var city_from = req.pathParams.cityFrom;
	var city_to = req.pathParams.cityTo;
	var paths = req.pathParams.amountOfPaths
    
	var city_from_key = db._query(aql`for city in cities filter city.name == ${to_right_register(city_from)} return city._key`).next();
	var city_to_key = db._query(aql`for city in cities filter city.name == ${to_right_register(city_to)} return city._key`).next();

    if (city_to_key == null || city_from_key == null) res.throw(err_city);

	var aql_req = aql`FOR p IN any K_SHORTEST_PATHS concat('cities/', ${city_from_key}) TO concat('cities/', ${city_to_key})
					  GRAPH 'roads'
					  OPTIONS {
					      weightAttribute: 'distance',
					      defaultWeight: 0
					          }
					      LIMIT ${Number(paths)}
					      RETURN {
					          places: p.vertices[*].name,
					          travel_distance: p.edges[*].distance,
					          travel_distance_total: CONCAT('~ ', ROUND(SUM(p.edges[*].distance)), ' km')
					      }`

	const answer = db._query(aql_req);
    	
    	if (answer['_documents'].length == 0){
    		res.send(err_way);
    	}else{
    		res.send(answer);
		}
})
.response(joi.array().items(
    joi.string().required()
).required(), 'List of entry keys.')
.summary('Returns a few shortest path between cities with distance.')
.description('Returns a few shortest path between cities with distance.');


router.get('/time-distance/:cityFrom/:cityTo/:amountOfPaths', function (req, res) {

	var city_from = req.pathParams.cityFrom;
	var city_to = req.pathParams.cityTo;
	var paths = req.pathParams.amountOfPaths
    
	var city_from_key = db._query(aql`for city in cities filter city.name == ${to_right_register(city_from)} return city._key`).next();
	var city_to_key = db._query(aql`for city in cities filter city.name == ${to_right_register(city_to)} return city._key`).next();

    if (city_to_key == null || city_from_key == null) res.throw(err_city);

		var aql_req = aql`FOR p IN any K_SHORTEST_PATHS concat('cities/', ${city_from_key}) TO concat('cities/', ${city_to_key})
					  GRAPH 'roads'
					  OPTIONS {
					      weightAttribute: 'distance',
					      defaultWeight: 0
					          }
					      LIMIT ${Number(paths)}
					      RETURN {
					          places: p.vertices[*].name,
					          travel_distance: p.edges[*].distance,
					          travel_distance_total: CONCAT('~ ', ROUND(SUM(p.edges[*].distance)), ' km'),
					          places: p.vertices[*].name,
					          travel_time: p.edges[*].time,
					          travel_time_total: CONCAT('~ ', ROUND(SUM(p.edges[*].time)/60), ' hours')
					      }`

		const answer = db._query(aql_req);
    	
    	if (answer['_documents'].length == 0){
    		res.send(err_way);
    	}else{
    		res.send(answer);
		}
})
.response(joi.array().items(
    joi.string().required()
).required(), 'List of entry keys.')
.summary('Returns a few shortest path between cities with distance and time.')
.description('Returns a few shortest path between cities with distance and time.');