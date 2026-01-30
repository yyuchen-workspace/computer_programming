<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Guide extends Model
{
    protected $fillable = [
        'title',
        'hero_name',
        'content',
        'author',
        'views',
    ];

    protected $casts = [
        'views' => 'integer',
    ];
}