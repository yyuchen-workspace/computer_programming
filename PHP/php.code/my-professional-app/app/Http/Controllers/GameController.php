<?php

namespace App\Http\Controllers;

use App\Game\HeroFactory;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class GameController extends Controller
{
    /**
     * 測試除錯端點 - 顯示克里希英雄資料
     *
     * 這個方法示範如何使用 HeroFactory 建立英雄物件
     * 你可以在這裡設置中斷點來進行除錯
     */
    public function testDebug(): JsonResponse
    {
        // 使用工廠建立克里希英雄物件
        $krixi = HeroFactory::createKrixi();

        // ===== 在這裡設置中斷點 =====
        $heroName = $krixi->name;  // ← 🔴 點這裡左側設中斷點

        // 當程式暫停時，可以在 Debug Console 輸入：
        // $krixi->name
        // $krixi->stats->getHp()
        // 查看即時資料！

        $heroHp = $krixi->stats->getHp();
        $heroAtk = $krixi->stats->getAtk();

        // 計算總傷害
        $totalDamage = $heroAtk * 1.5;  // ← 也可以在這裡設中斷點

        return response()->json([
            'hero' => $heroName,
            'stats' => [
                'hp' => $heroHp,
                'atk' => $heroAtk,
                'totalDamage' => $totalDamage,
            ],
            'skills' => $krixi->skills,
            'debug_message' => '如果你看到這個訊息，代表程式已經執行完畢了！',
        ]);
    }

    /**
     * 顯示所有英雄列表
     */
    public function index(): JsonResponse
    {
        $heroes = HeroFactory::getAllHeroes();

        return response()->json([
            'heroes' => array_map(function ($hero) {
                return [
                    'name' => $hero->name,
                    'hp' => $hero->stats->getHp(),
                    'atk' => $hero->stats->getAtk(),
                    'skills' => array_map(fn($skill) => $skill->name, $hero->skills),
                ];
            }, $heroes),
        ]);
    }

    /**
     * 顯示特定英雄資訊
     */
    public function show(string $heroName): JsonResponse
    {
        $hero = HeroFactory::create($heroName);

        if (!$hero) {
            return response()->json([
                'error' => '找不到英雄: ' . $heroName,
                'available_heroes' => ['krixi', 'vane', '克里希', '凡恩'],
            ], 404);
        }

        return response()->json([
            'name' => $hero->name,
            'article' => $hero->article,
            'stats' => [
                'hp' => $hero->stats->getHp(),
                'mp' => $hero->stats->getMp(),
                'atk' => $hero->stats->getAtk(),
                'def' => $hero->stats->getDef(),
            ],
            'skills' => $hero->skills,
        ]);
    }
}
