<?php
/**
 * Created by PhpStorm.
 * User: john
 * Date: 2019-11-16
 * Time: 17:09
 */

namespace App\Services;


use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class AnimeService
{
    const animeTable = "anime";
    const animeLinks = "anime_links";
    const animeAccess = "anime_access";

    public function searchAnime(Request $request)
    {
        $builder = DB::table(self::animeTable)->select("*");
        if ($request->input("title")) {
            $titleF = $request->input('title');
            $builder = $builder->where('title', 'like', "%$titleF%");
        }
        if ($request->input('year')) {
            $builder = $builder->where('year', $request->input('year'));
        }
        if ($request->input('description')) {
            $descrF = strtolower($request->input('description'));
            $builder = $builder->whereRaw("LOWER(description) LIKE '%$descrF%'");
        }
        $builder = $builder->orderBy('id', 'desc');
        return $builder->get();
    }

    public function addAnime($user_id, $title, $description, $public, $year)
    {
        return DB::table(self::animeTable)->insert(
            [
                'title' => $title,
                'description' => $description,
                'year' => $year,
                'public' => $public,
                'owner_id' => $user_id,
            ]
        );
    }

    public function addAnimeLink($animeId, $link)
    {
        return DB::table(self::animeTable)->insert(
            [
                'anime_id' => $animeId,
                'content' => $link,
            ]
        );
    }

    public function getAnimeLinks($animeId)
    {
        return DB::table(self::animeLinks)->where('anime_id', $animeId)->get();
    }

    public function addAnimeAccess($animeId, $userId)
    {
        $anime = $this->getAnimeById($animeId);
        if ($anime) {
            return DB::table(self::animeAccess)->insert(
                [
                    'anime_id' => $anime->id,
                    'user_id' => $userId
                ]
            );
        }
        return false;
    }

    public function getAnimeAccess($animeId, $userId)
    {
        return DB::table(self::animeAccess)->where(
            'anime_id', $animeId)->where('user_id', $userId)->first();
    }


    public function getAnimeById($animeId)
    {
        return DB::table(self::animeTable)->where('id', $animeId)->first();
    }

    public function getAnimeDetails($animeId, $userId)
    {

        $anime = $this->getAnimeById($animeId);
        if (!$anime) {
            return null;
        }

        $data = ['anime' => $anime];

        if ($anime->public || ($anime->owner_id == $userId) || $this->getAnimeAccess($animeId, $userId)) {
            $data['links'] = $this->getAnimeLinks($animeId);
        }

        if ($anime->owner_id == $userId) {
            $data['access_token'] = TokenService::generateToken($animeId);
        }

        return $data;
    }

    public function getMyAnime($userId)
    {
        return DB::table(self::animeTable)
            ->join(self::animeAccess, self::animeTable . 'id', '=', self::animeAccess . "anime_id")
            ->where(self::animeTable . 'owner_id', $userId)->orWhere(self::animeAccess . "user_id", $userId)->get();
    }

    public function tryGetAnimeAccess($animeId, $token)
    {
        return TokenService::generateToken($animeId) == $token;
    }


}