<?php

namespace App\Http\Controllers;


use App\Services\AnimeService;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;

class AnimeController extends Controller
{
    /** @var AnimeService $animeService */
    private $animeService;

    public function __construct(AnimeService $service)
    {
        $this->animeService = $service;
    }

    public function addAnime(Request $request)
    {
        try {
            $this->validate($request, [
                'title' => 'required|max:200',
                'description' => 'required|max:2000',
                'public' => 'required|boolean',
                'year' => 'integer'
            ]);

        } catch (ValidationException $e) {
            return response()->json(["error" => $e], 422);
        }

        $user = $request->user();
        $title = $request->input('title');
        $description = $request->input('description');
        $year = $request->input('year') ?? 0;
        $public = $request->input('public');

        $ok = $this->animeService->addAnime($user->id, $title, $description, $public, $year);

        return response()->json(["result" => $ok]);
    }

    public function addAnimeLink(Request $request, $animeId)
    {
        $user = $request->user();

        $anime = $this->animeService->getAnimeById($animeId);

        if (!$anime) {
            return response()->json(["error" => 'not found'], 404);
        }

        if ($anime->owner_id != $user->id) {
            return response()->json(["error" => 'Unauthorized'], 403);
        }

        $this->animeService->addAnimeLink($animeId, $request->input('link'));

        return response()->json(["result" => "ok"]);
    }


    public function listMyAnime(Request $request)
    {
        $user = $request->user();

        return response()->json(["result" => $this->animeService->getMyAnime($user->id)]);
    }

    public function listAnime(Request $request)
    {
        $anime = $this->animeService->searchAnime($request);
        return response()->json(["result" => $anime]);
    }

    public function getAccess(Request $request)
    {
        if ($request->has('anime') && $request->has('token')) {
            $animeId = $request->input('anime');
            $ok = $this->animeService->tryGetAnimeAccess($animeId, $request->input('token'));
            if ($ok) {
                return response()->json(["result" => $this->animeService->addAnimeAccess($animeId, $request->user()->id)]);
            }
        }
        return response()->json(["error" => "not ok"]);
    }

    public function detailsAnime(Request $request, $animeId)
    {
        $details = $this->animeService->getAnimeDetails($animeId, $request->user()->id);
        if ($details) {
            return response()->json(["result" => $details]);
        }
        return response()->json(["error" => 'not found'], 404);
    }

}
