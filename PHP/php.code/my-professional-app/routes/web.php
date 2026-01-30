<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\GameController;
use App\Http\Controllers\GuideController;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/hello', function () {
    return view('greeting', ['name' => 'Professional App User']);
});

// ===== 遊戲相關路由 =====

// 測試除錯端點 - 顯示克里希英雄資料
Route::get('/test-debug', [GameController::class, 'testDebug']);

// 顯示所有英雄列表
Route::get('/heroes', [GameController::class, 'index']);

// 顯示特定英雄資訊 (可以用英文或中文名稱)
// 例如: /heroes/krixi 或 /heroes/克里希
Route::get('/heroes/{heroName}', [GameController::class, 'show']);

Route::resource('guides', GuideController::class);
