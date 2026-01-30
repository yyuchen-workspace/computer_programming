<?php

namespace App\Game;

/**
 * 英雄工廠類別
 *
 * 負責建立各種英雄物件，集中管理英雄資料
 */
class HeroFactory
{
    /**
     * 建立克里希英雄
     */
    public static function createKrixi(): Hero
    {
        // 1. 準備數值物件 (零件 A)
        $stats = new Stats(3200, 500, 180, 120);

        // 2. 準備技能陣列 (零件 B)
        $skills = [
            new Skill("蝶影穿花", "向指定方向扔出飛舞的飛蛾..."),
            new Skill("落葉歸根", "召喚自然力量將敵人擊飛..."),
            new Skill("月落星沉", "召喚流星雨..."),
        ];

        // 3. 準備教學文章 (零件 C)
        $article = "克里希是一名強大的遠程消耗型法師。";

        // 4. 組裝成英雄物件
        return new Hero("克里希", $stats, $skills, $article);
    }

    /**
     * 建立凡恩英雄
     */
    public static function createVane(): Hero
    {
        $stats = new Stats(100, 80, 40, 20);

        $skills = [
            new Skill("獵手", "...說明略..."),
            new Skill("血腥獵殺", "...說明略..."),
            new Skill("送葬詛咒", "...說明略..."),
            new Skill("水銀彈幕", "...說明略..."),
        ];

        $article = "文章略";

        return new Hero("凡恩", $stats, $skills, $article);
    }

    /**
     * 根據英雄名稱建立英雄
     *
     * @param string $heroName 英雄名稱
     * @return Hero|null
     */
    public static function create(string $heroName): ?Hero
    {
        return match (strtolower($heroName)) {
            'krixi', '克里希' => self::createKrixi(),
            'vane', '凡恩' => self::createVane(),
            default => null,
        };
    }

    /**
     * 取得所有可用的英雄列表
     *
     * @return array<Hero>
     */
    public static function getAllHeroes(): array
    {
        return [
            self::createKrixi(),
            self::createVane(),
        ];
    }
}
