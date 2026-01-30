<?php

namespace App\Game;

class Skill
{
    public $name;        // 技能名稱
    public $description; // 技能描述

    public function __construct(string $sourceName, string $sourceDescription)
    {
        $this->name = $sourceName;
        $this->description = $sourceDescription;
    }
}
