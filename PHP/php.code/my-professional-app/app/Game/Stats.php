<?php

namespace App\Game;

class Stats
{
    private $hp;  // 生命值
    private $mp;  // 法力值
    private $atk; // 攻擊力
    private $def; // 防禦力

    public function __construct(int $sourceHp, int $sourceMp, int $sourceAtk, int $sourceDef)
    {
        $this->hp = $sourceHp;
        $this->mp = $sourceMp;
        $this->atk = $sourceAtk;
        $this->def = $sourceDef;
    }

    public function getHp(): int
    {
        return $this->hp;
    }

    public function getMp(): int
    {
        return $this->mp;
    }

    public function getAtk(): int
    {
        return $this->atk;
    }

    public function getDef(): int
    {
        return $this->def;
    }

    public function takeDamage(int $damage): void
    {
        $this->hp -= $damage;
        if ($this->hp < 0) {
            $this->hp = 0;
        }
    }
}
