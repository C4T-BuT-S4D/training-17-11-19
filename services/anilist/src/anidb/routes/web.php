<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It is a breeze. Simply tell Lumen the URIs it should respond to
| and give it the Closure to call when that URI is requested.
|
*/

$router->get('/', function () use ($router) {
    return $router->app->version();
});


$router->group(["middleware" => ["auth:api"]], function () use ($router) {
    $router->get('/anime', 'AnimeController@listAnime');
    $router->post('/anime', 'AnimeController@addAnime');
    $router->post('/anime/{id}', 'AnimeController@addAnimeLink');
    $router->get('/anime/{id}', 'AnimeController@detailsAnime');
    $router->get('/my_anime', 'AnimeController@listMyAnime');
    $router->get('/get_access', 'AnimeController@getAccess');

});
