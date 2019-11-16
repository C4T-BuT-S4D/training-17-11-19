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

$router->get('/api/db', function () use ($router) {
    return $router->app->version();
});


$router->group(["middleware" => ["auth:api"]], function () use ($router) {
    $router->get('/api/db/anime', 'AnimeController@listAnime');
    $router->post('/api/db/anime', 'AnimeController@addAnime');
    $router->post('/api/db/anime/{id}', 'AnimeController@addAnimeLink');
    $router->get('/api/db/anime/{id}', 'AnimeController@detailsAnime');
    $router->get('/api/db/my_anime', 'AnimeController@listMyAnime');
    $router->get('/api/db/get_access', 'AnimeController@getAccess');
});
