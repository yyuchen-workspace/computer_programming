<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('guides', function (Blueprint $table) {
            $table->id();
            $table->string('title');                // 攻略標題
            $table->string('hero_name');            // 英雄名稱
            $table->text('content');                // 攻略內容
            $table->string('author')->nullable();   // 作者名稱
            $table->integer('views')->default(0);   // 瀏覽次數
            $table->timestamps();                   // created_at, updated_at
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('guides');
    }
};
