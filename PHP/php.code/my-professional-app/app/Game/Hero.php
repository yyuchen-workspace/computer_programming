<?php

namespace App\Game;

class Hero
{
    public $name;    // 預備裝 角色名稱字串變數
    public $stats;   // 準備裝『數值物件』的變數
    public $skills;  // 準備裝『技能物件』的陣列變數
    public $article; // 預備來裝 教學文章 變數

    public function __construct(string $sourceName, Stats $sourceStats, array $sourceSkills, string $sourceArticle)
    {
        $this->name = $sourceName;
        $this->stats = $sourceStats;
        $this->skills = $sourceSkills;
        $this->article = $sourceArticle;
    }
}
