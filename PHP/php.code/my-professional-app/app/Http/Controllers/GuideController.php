<?php

namespace App\Http\Controllers;

use App\Models\Guide;
use Illuminate\Http\Request;

class GuideController extends Controller
{
    // 顯示所有攻略
    public function index()
    {
        $guides = Guide::orderBy('created_at', 'desc')->get();
        return view('guides.index', compact('guides'));
    }

    // 顯示新增攻略表單
    public function create()
    {
        return view('guides.create');
    }

    // 儲存新攻略
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'hero_name' => 'required|max:255',
            'content' => 'required',
            'author' => 'nullable|max:255',
        ]);

        Guide::create($validated);

        return redirect()->route('guides.index')
            ->with('success', '攻略新增成功！');
    }

    // 顯示單一攻略
    public function show(Guide $guide)
    {
        // 增加瀏覽次數
        $guide->increment('views');

        return view('guides.show', compact('guide'));
    }

    // 顯示編輯表單
    public function edit(Guide $guide)
    {
        return view('guides.edit', compact('guide'));
    }

    // 更新攻略
    public function update(Request $request, Guide $guide)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'hero_name' => 'required|max:255',
            'content' => 'required',
            'author' => 'nullable|max:255',
        ]);

        $guide->update($validated);

        return redirect()->route('guides.show', $guide)
            ->with('success', '攻略更新成功！');
    }

    // 刪除攻略
    public function destroy(Guide $guide)
    {
        $guide->delete();

        return redirect()->route('guides.index')
            ->with('success', '攻略已刪除！');
    }
}
