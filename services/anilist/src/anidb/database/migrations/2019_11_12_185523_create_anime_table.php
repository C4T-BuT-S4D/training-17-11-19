<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateAnimeTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('anime', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string("title", 200);
            $table->string("description", 2000);
            $table->boolean("public");
            $table->unsignedInteger("year");
            $table->integer('owner_id');
            $table->timestamps();
        });

        Schema::create('anime_links', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->integer("anime_id");
            $table->string("content", 200);
            $table->timestamps();
        });

        Schema::create('anime_access', function (Blueprint $table) {
            $table->bigInteger('id');
            $table->integer('anime_id');
            $table->integer('user_id');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('anime');
        Schema::dropIfExists('anime_links');
        Schema::dropIfExists('anime_access');
    }
}
