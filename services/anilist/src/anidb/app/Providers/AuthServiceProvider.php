<?php

namespace App\Providers;

use App\User;
use Illuminate\Support\Facades\Gate;
use Illuminate\Auth\GenericUser;

use Illuminate\Support\ServiceProvider;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Boot the authentication services for the application.
     *
     * @return void
     */
    public function boot()
    {
        // Here you may define how you wish users to be authenticated for your Lumen
        // application. The callback which receives the incoming request instance
        // should return either a User instance or null. You're free to obtain
        // the User instance via an API token or any other method necessary.

        $this->app['auth']->viaRequest('api', function ($request) {

            $sessionId = $request->cookie('session');
            if ($sessionId && $sessionId != '') {
                $sessionUser = $this->app['redis']->get($sessionId);
                $user = json_decode($sessionUser, true);
                if ($user && $user['id']) {
                    return new GenericUser(['id' => $user['id'], 'name' => $user['name']]);
                }
            }
            return null;
        });
    }
}
