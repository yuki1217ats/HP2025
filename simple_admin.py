#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import shutil
from datetime import datetime
import subprocess
import re

class SimpleAdminTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ブログ管理ツール - Simple Blog Admin")
        self.root.geometry("1000x700")
        
        # プロジェクトパス
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.posts_file = os.path.join(self.project_path, "posts.json")
        self.images_dir = os.path.join(self.project_path, "images")
        self.blog_js_file = os.path.join(self.project_path, "blog.js")
        
        # 画像ディレクトリ作成
        os.makedirs(self.images_dir, exist_ok=True)
        
        # 投稿データ
        self.posts = []
        
        # UI作成
        self.create_ui()
        
        # データ読み込み
        self.load_posts()
        
    def create_ui(self):
        """UIを作成"""
        # ノートブックでタブを作成
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 投稿管理タブ
        self.posts_frame = ttk.Frame(notebook)
        notebook.add(self.posts_frame, text="投稿管理")
        self.create_posts_tab()
        
        # ギャラリータブ
        self.gallery_frame = ttk.Frame(notebook)
        notebook.add(self.gallery_frame, text="ギャラリー管理")
        self.create_gallery_tab()
        
        # Git操作タブ
        self.git_frame = ttk.Frame(notebook)
        notebook.add(self.git_frame, text="Git操作")
        self.create_git_tab()
    
    def create_posts_tab(self):
        """投稿管理タブを作成"""
        # 左側：投稿リスト
        left_frame = ttk.Frame(self.posts_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        ttk.Label(left_frame, text="投稿一覧", font=("", 14, "bold")).pack(pady=(0, 10))
        
        # リストボックス
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill='both', expand=True)
        
        self.posts_listbox = tk.Listbox(list_frame, width=40)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.posts_listbox.yview)
        self.posts_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.posts_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.posts_listbox.bind('<<ListboxSelect>>', self.on_post_select)
        
        # ボタン
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text="新規投稿", command=self.new_post).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="削除", command=self.delete_post).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="更新", command=self.refresh_posts_list).pack(side='left', padx=5)
        
        # 右側：投稿編集
        right_frame = ttk.Frame(self.posts_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # タイトル
        ttk.Label(right_frame, text="タイトル:").grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = ttk.Entry(right_frame, width=50)
        self.title_entry.grid(row=0, column=1, sticky='ew', pady=5)
        
        # 日付
        ttk.Label(right_frame, text="日付:").grid(row=1, column=0, sticky='w', pady=5)
        self.date_entry = ttk.Entry(right_frame, width=20)
        self.date_entry.grid(row=1, column=1, sticky='w', pady=5)
        
        # タグ
        ttk.Label(right_frame, text="タグ（カンマ区切り）:").grid(row=2, column=0, sticky='w', pady=5)
        self.tags_entry = ttk.Entry(right_frame, width=50)
        self.tags_entry.grid(row=2, column=1, sticky='ew', pady=5)
        
        # 抜粋
        ttk.Label(right_frame, text="抜粋:").grid(row=3, column=0, sticky='nw', pady=5)
        self.excerpt_text = tk.Text(right_frame, width=50, height=3)
        self.excerpt_text.grid(row=3, column=1, sticky='ew', pady=5)
        
        # 本文
        ttk.Label(right_frame, text="本文:").grid(row=4, column=0, sticky='nw', pady=5)
        self.content_text = scrolledtext.ScrolledText(right_frame, width=50, height=15)
        self.content_text.grid(row=4, column=1, sticky='nsew', pady=5)
        
        # ボタン
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=5, column=1, sticky='w', pady=10)
        
        ttk.Button(btn_frame, text="画像を挿入", command=self.insert_image).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="保存", command=self.save_post).pack(side='left', padx=5)
        
        # グリッド設定
        right_frame.columnconfigure(1, weight=1)
        right_frame.rowconfigure(4, weight=1)
    
    def create_gallery_tab(self):
        """ギャラリータブを作成"""
        # アップロードボタン
        ttk.Button(self.gallery_frame, text="画像をアップロード", 
                  command=self.upload_images).pack(pady=10)
        
        # 画像リスト
        list_frame = ttk.Frame(self.gallery_frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.image_listbox = tk.Listbox(list_frame, height=20)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.image_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # ボタン
        btn_frame = ttk.Frame(self.gallery_frame)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text="削除", command=self.delete_image).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="更新", command=self.refresh_gallery).pack(side='left', padx=5)
        
        # 初期表示
        self.refresh_gallery()
    
    def create_git_tab(self):
        """Git操作タブを作成"""
        # ボタン
        btn_frame = ttk.Frame(self.git_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Git Status", command=self.git_status).pack(pady=5)
        ttk.Button(btn_frame, text="Git Add All", command=self.git_add).pack(pady=5)
        ttk.Button(btn_frame, text="Git Commit", command=self.git_commit).pack(pady=5)
        ttk.Button(btn_frame, text="Git Push", command=self.git_push).pack(pady=5)
        
        # 出力エリア
        ttk.Label(self.git_frame, text="Git出力:").pack()
        self.git_output = scrolledtext.ScrolledText(self.git_frame, width=80, height=20)
        self.git_output.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_posts(self):
        """投稿データを読み込み"""
        # まずblog.jsから現在の投稿を読み込む
        try:
            with open(self.blog_js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # posts配列を抽出
            match = re.search(r'this\.posts = \[(.*?)\];', content, re.DOTALL)
            if match:
                posts_str = '[' + match.group(1) + ']'
                # JavaScriptの構文をPython用に変換
                posts_str = re.sub(r'(\w+):', r'"\1":', posts_str)  # key: → "key":
                posts_str = posts_str.replace("'", '"')  # single quotes → double quotes
                self.posts = json.loads(posts_str)
        except Exception as e:
            print(f"blog.js読み込みエラー: {e}")
            self.posts = []
        
        # posts.jsonが存在する場合は追加で読み込む
        if os.path.exists(self.posts_file):
            try:
                with open(self.posts_file, 'r', encoding='utf-8') as f:
                    json_posts = json.load(f)
                    # 重複を避けるため、IDで管理
                    existing_ids = {p['id'] for p in self.posts}
                    for post in json_posts:
                        if post['id'] not in existing_ids:
                            self.posts.append(post)
            except Exception as e:
                print(f"posts.json読み込みエラー: {e}")
        
        self.refresh_posts_list()
    
    def save_posts(self):
        """投稿データを保存"""
        # posts.jsonに保存
        with open(self.posts_file, 'w', encoding='utf-8') as f:
            json.dump(self.posts, f, ensure_ascii=False, indent=2)
        
        # blog.jsを更新
        self.update_blog_js()
        
        messagebox.showinfo("成功", "投稿を保存しました。")
    
    def update_blog_js(self):
        """blog.jsファイルを更新"""
        try:
            with open(self.blog_js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # posts配列を生成
            posts_lines = []
            for i, post in enumerate(self.posts):
                lines = []
                lines.append("            {")
                lines.append(f"                id: '{post['id']}',")
                lines.append(f"                date: '{post['date']}',")
                lines.append(f"                title: '{post['title']}',")
                
                # contentの改行を\\nに変換
                content_escaped = post['content'].replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")
                lines.append(f"                content: '{content_escaped}',")
                
                # excerptの処理
                excerpt_escaped = post['excerpt'].replace('\\', '\\\\').replace('\n', ' ').replace("'", "\\'")
                lines.append(f"                excerpt: '{excerpt_escaped}',")
                
                # tags
                tags_str = ', '.join([f"'{tag}'" for tag in post['tags']])
                lines.append(f"                tags: [{tags_str}]")
                
                if i < len(self.posts) - 1:
                    lines.append("            },")
                else:
                    lines.append("            }")
                
                posts_lines.extend(lines)
            
            posts_str = '\n'.join(posts_lines)
            
            # posts配列を置換
            pattern = r'(this\.posts = \[)(.*?)(\];)'
            replacement = f'\\1\n{posts_str}\n        \\3'
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            with open(self.blog_js_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("blog.jsを更新しました")
        except Exception as e:
            print(f"blog.js更新エラー: {e}")
            messagebox.showerror("エラー", f"blog.js更新エラー: {e}")
    
    def refresh_posts_list(self):
        """投稿一覧を更新"""
        self.posts_listbox.delete(0, tk.END)
        
        # 日付でソート（新しい順）
        sorted_posts = sorted(self.posts, key=lambda x: x['date'], reverse=True)
        
        for post in sorted_posts:
            self.posts_listbox.insert(tk.END, f"{post['date']} - {post['title']}")
    
    def on_post_select(self, event):
        """投稿選択時"""
        selection = self.posts_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        sorted_posts = sorted(self.posts, key=lambda x: x['date'], reverse=True)
        post = sorted_posts[index]
        
        # フォームに値を設定
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, post['title'])
        
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, post['date'])
        
        self.tags_entry.delete(0, tk.END)
        self.tags_entry.insert(0, ', '.join(post['tags']))
        
        self.excerpt_text.delete('1.0', tk.END)
        self.excerpt_text.insert('1.0', post['excerpt'])
        
        self.content_text.delete('1.0', tk.END)
        self.content_text.insert('1.0', post['content'])
    
    def new_post(self):
        """新規投稿"""
        # フォームをクリア
        self.title_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.tags_entry.delete(0, tk.END)
        self.excerpt_text.delete('1.0', tk.END)
        self.content_text.delete('1.0', tk.END)
        
        # リストボックスの選択を解除
        self.posts_listbox.selection_clear(0, tk.END)
    
    def save_post(self):
        """投稿を保存"""
        title = self.title_entry.get().strip()
        date = self.date_entry.get().strip()
        tags_str = self.tags_entry.get().strip()
        excerpt = self.excerpt_text.get('1.0', tk.END).strip()
        content = self.content_text.get('1.0', tk.END).strip()
        
        if not title or not date or not content:
            messagebox.showerror("エラー", "タイトル、日付、本文は必須です。")
            return
        
        # タグを配列に変換
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # 抜粋が空の場合は本文から生成
        if not excerpt:
            excerpt = content[:100] + '...' if len(content) > 100 else content
            excerpt = excerpt.replace('\n', ' ')
        
        # IDを生成
        post_id = date
        
        # 既存投稿の更新または新規追加
        existing_post = next((p for p in self.posts if p['id'] == post_id and p['title'] == title), None)
        
        post = {
            'id': post_id,
            'date': date,
            'title': title,
            'content': content,
            'excerpt': excerpt,
            'tags': tags
        }
        
        if existing_post:
            # 更新
            index = self.posts.index(existing_post)
            self.posts[index] = post
        else:
            # 新規追加
            self.posts.append(post)
        
        self.save_posts()
        self.refresh_posts_list()
    
    def delete_post(self):
        """選択した投稿を削除"""
        selection = self.posts_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "削除する投稿を選択してください。")
            return
        
        if messagebox.askyesno("確認", "選択した投稿を削除しますか？"):
            index = selection[0]
            sorted_posts = sorted(self.posts, key=lambda x: x['date'], reverse=True)
            post = sorted_posts[index]
            
            self.posts.remove(post)
            self.save_posts()
            self.refresh_posts_list()
            self.new_post()  # フォームをクリア
    
    def insert_image(self):
        """画像を挿入"""
        filename = filedialog.askopenfilename(
            title="画像を選択",
            filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.gif *.webp")]
        )
        
        if filename:
            # 画像をコピー
            basename = os.path.basename(filename)
            dest_path = os.path.join(self.images_dir, basename)
            shutil.copy2(filename, dest_path)
            
            # HTMLタグを挿入
            img_tag = f'<img src="images/{basename}" alt="{basename}" style="max-width: 100%; height: auto;">'
            self.content_text.insert(tk.INSERT, f"\n\n{img_tag}\n\n")
            
            self.refresh_gallery()
    
    def upload_images(self):
        """画像をアップロード"""
        filenames = filedialog.askopenfilenames(
            title="画像を選択",
            filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.gif *.webp")]
        )
        
        for filename in filenames:
            basename = os.path.basename(filename)
            dest_path = os.path.join(self.images_dir, basename)
            shutil.copy2(filename, dest_path)
        
        if filenames:
            self.refresh_gallery()
            messagebox.showinfo("成功", f"{len(filenames)}個の画像をアップロードしました。")
    
    def refresh_gallery(self):
        """ギャラリーを更新"""
        self.image_listbox.delete(0, tk.END)
        
        if os.path.exists(self.images_dir):
            for filename in sorted(os.listdir(self.images_dir)):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    self.image_listbox.insert(tk.END, filename)
    
    def delete_image(self):
        """選択した画像を削除"""
        selection = self.image_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "削除する画像を選択してください。")
            return
        
        filename = self.image_listbox.get(selection[0])
        if messagebox.askyesno("確認", f"画像 '{filename}' を削除しますか？"):
            os.remove(os.path.join(self.images_dir, filename))
            self.refresh_gallery()
    
    def run_git_command(self, command):
        """Gitコマンドを実行"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            output = f"$ {command}\n"
            if result.stdout:
                output += result.stdout + "\n"
            if result.stderr:
                output += result.stderr + "\n"
            
            self.git_output.insert(tk.END, output + "\n")
            self.git_output.see(tk.END)
            
            return result.returncode == 0
        except Exception as e:
            self.git_output.insert(tk.END, f"エラー: {str(e)}\n\n")
            return False
    
    def git_status(self):
        """Git status"""
        self.run_git_command("git status")
    
    def git_add(self):
        """Git add all"""
        self.run_git_command("git add .")
    
    def git_commit(self):
        """Git commit"""
        # コミットメッセージダイアログ
        dialog = tk.Toplevel(self.root)
        dialog.title("コミットメッセージ")
        dialog.geometry("400x150")
        
        ttk.Label(dialog, text="コミットメッセージ:").pack(pady=10)
        msg_entry = ttk.Entry(dialog, width=50)
        msg_entry.pack(pady=5)
        msg_entry.insert(0, f"Update blog posts - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        def do_commit():
            msg = msg_entry.get()
            if msg:
                self.run_git_command(f'git commit -m "{msg}"')
                dialog.destroy()
        
        ttk.Button(dialog, text="コミット", command=do_commit).pack(pady=10)
        msg_entry.focus()
        msg_entry.bind('<Return>', lambda e: do_commit())
    
    def git_push(self):
        """Git push"""
        if messagebox.askyesno("確認", "GitHubにプッシュしますか？"):
            self.run_git_command("git push origin main")
    
    def run(self):
        """アプリケーションを実行"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleAdminTool()
    app.run()