<?php

namespace App\Services;


class TokenService
{
    const secret = 'abacaba';

    public static function generateToken($data)
    {
        return hash_hmac('sha256', $data, self::secret);
    }
}