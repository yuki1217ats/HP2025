#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import shutil
from datetime import datetime
import subprocess
import sys
from PIL import Image, ImageTk
import re

class HPAdminTool:
    def __init__(self, root):
        self.root = root
        self.root.title("HP管理ツール - My Personal Space")
        self.root.geometry("1000x700")
        
        # プロジェクトパス
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.posts_file = os.path.join(self.project_path, "posts.json")
        self.images_dir = os.path.join(self.project_path, "images")
        self.blog_js_file = os.path.join(self.project_path, "blog.js")
        
        # 画像ディレクトリ作成
        os.makedirs(self.images_dir, exist_ok=True)
        
        # GUI構築
        self.setup_ui()
        
        # データ読み込み
        self.load_posts()
        
    def setup_ui(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # タブ作成
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ブログ投稿タブ
        self.blog_frame = ttk.Frame(notebook)
        notebook.add(self.blog_frame, text="ブログ投稿")
        self.setup_blog_tab()
        
        # ギャラリータブ
        self.gallery_frame = ttk.Frame(notebook)
        notebook.add(self.gallery_frame, text="ギャラリー管理")
        self.setup_gallery_tab()
        
        # 設定タブ
        self.settings_frame = ttk.Frame(notebook)
        notebook.add(self.settings_frame, text="設定・プッシュ")
        self.setup_settings_tab()
        
        # ウィンドウサイズ調整
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def setup_blog_tab(self):
        # 左側：投稿リスト
        left_frame = ttk.Frame(self.blog_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        ttk.Label(left_frame, text="投稿一覧", font=("", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # 投稿リストボックス
        self.posts_listbox = tk.Listbox(left_frame, width=30)
        self.posts_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.posts_listbox.bind('<<ListboxSelect>>', self.on_post_select)
        
        # ボタンフレーム
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=2, column=0, sticky=tk.W)
        
        ttk.Button(button_frame, text="新規投稿", command=self.new_post).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="削除", command=self.delete_post).grid(row=0, column=1)
        
        # 右側：投稿編集
        right_frame = ttk.Frame(self.blog_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # タイトル
        ttk.Label(right_frame, text="タイトル").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(right_frame, width=50)
        self.title_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 日付
        ttk.Label(right_frame, text="日付").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.date_entry = ttk.Entry(right_frame, width=20)
        self.date_entry.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # タグ
        ttk.Label(right_frame, text="タグ（カンマ区切り）").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.tags_entry = ttk.Entry(right_frame, width=50)
        self.tags_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 内容
        ttk.Label(right_frame, text="内容").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.content_text = scrolledtext.ScrolledText(right_frame, width=60, height=15)
        self.content_text.grid(row=7, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 画像挿入ボタン
        image_button_frame = ttk.Frame(right_frame)
        image_button_frame.grid(row=8, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Button(image_button_frame, text="画像を挿入", command=self.insert_image).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(image_button_frame, text="保存", command=self.save_post).grid(row=0, column=1)
        
        # グリッド設定
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(7, weight=1)
        self.blog_frame.columnconfigure(1, weight=2)
        self.blog_frame.rowconfigure(0, weight=1)
        
    def setup_gallery_tab(self):
        # 画像アップロードフレーム
        upload_frame = ttk.LabelFrame(self.gallery_frame, text="画像アップロード", padding="10")
        upload_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(upload_frame, text="画像を選択してアップロード", command=self.upload_images).grid(row=0, column=0)
        
        # 画像一覧フレーム
        gallery_frame = ttk.LabelFrame(self.gallery_frame, text="ギャラリー", padding="10")
        gallery_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 画像一覧用キャンバス
        self.gallery_canvas = tk.Canvas(gallery_frame, height=400)
        self.gallery_scrollbar = ttk.Scrollbar(gallery_frame, orient="vertical", command=self.gallery_canvas.yview)
        self.gallery_canvas.configure(yscrollcommand=self.gallery_scrollbar.set)
        
        self.gallery_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.gallery_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 画像表示用フレーム
        self.gallery_content_frame = ttk.Frame(self.gallery_canvas)
        self.gallery_canvas.create_window((0, 0), window=self.gallery_content_frame, anchor="nw")
        
        # グリッド設定
        self.gallery_frame.columnconfigure(0, weight=1)
        self.gallery_frame.rowconfigure(1, weight=1)
        gallery_frame.columnconfigure(0, weight=1)
        gallery_frame.rowconfigure(0, weight=1)
        
        # 画像一覧更新
        self.refresh_gallery()
        
    def setup_settings_tab(self):
        # Git設定フレーム
        git_frame = ttk.LabelFrame(self.settings_frame, text="Git設定", padding="10")
        git_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 自動プッシュ設定
        self.auto_push_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(git_frame, text="保存時に自動でGitHubにプッシュする", variable=self.auto_push_var).grid(row=0, column=0, sticky=tk.W)
        
        # 手動プッシュボタン
        button_frame = ttk.Frame(git_frame)
        button_frame.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        ttk.Button(button_frame, text="手動プッシュ", command=self.manual_push).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Git状態確認", command=self.check_git_status).grid(row=0, column=1)
        
        # ログ表示
        log_frame = ttk.LabelFrame(self.settings_frame, text="ログ", padding="10")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=80, height=20)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # グリッド設定
        self.settings_frame.columnconfigure(0, weight=1)
        self.settings_frame.rowconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def log(self, message):
        """ログ出力"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def load_posts(self):
        """投稿データを読み込み"""
        self.posts = []
        
        # posts.jsonから読み込み（存在する場合）
        if os.path.exists(self.posts_file):
            try:
                with open(self.posts_file, 'r', encoding='utf-8') as f:
                    self.posts = json.load(f)
            except Exception as e:
                self.log(f"posts.json読み込みエラー: {e}")
        
        self.refresh_posts_list()
        
    def save_posts_to_json(self):
        """投稿データをJSONファイルに保存"""
        try:
            with open(self.posts_file, 'w', encoding='utf-8') as f:
                json.dump(self.posts, f, ensure_ascii=False, indent=2)
            self.log("posts.jsonを更新しました")
        except Exception as e:
            self.log(f"posts.json保存エラー: {e}")
            
    def update_blog_js(self):
        """blog.jsファイルを更新"""
        try:
            # blog.jsを読み込み
            with open(self.blog_js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # posts配列を置換
            posts_json = json.dumps(self.posts, ensure_ascii=False, indent=12)
            
            # SimpleBlogSystemクラス内のposts配列を置換
            pattern = r'(this\.posts = \[)[^;]*(\];)'
            replacement = f'\\1{posts_json[1:-1]}\\2'
            
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # ファイルに書き込み
            with open(self.blog_js_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            self.log("blog.jsを更新しました")
            
        except Exception as e:
            self.log(f"blog.js更新エラー: {e}")
            
    def refresh_posts_list(self):
        """投稿リスト更新"""
        self.posts_listbox.delete(0, tk.END)
        for post in sorted(self.posts, key=lambda x: x['date'], reverse=True):
            self.posts_listbox.insert(tk.END, f"{post['date']} - {post['title']}")
            
    def on_post_select(self, event):
        """投稿選択時"""
        selection = self.posts_listbox.curselection()
        if selection:
            index = selection[0]
            post = sorted(self.posts, key=lambda x: x['date'], reverse=True)[index]
            
            # フォームに値を設定
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, post['title'])
            
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, post['date'])
            
            self.tags_entry.delete(0, tk.END)
            self.tags_entry.insert(0, ', '.join(post['tags']))
            
            self.content_text.delete('1.0', tk.END)
            self.content_text.insert('1.0', post['content'])
            
    def new_post(self):
        """新規投稿"""
        self.title_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.tags_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)
        
    def save_post(self):
        """投稿保存"""
        title = self.title_entry.get().strip()
        date = self.date_entry.get().strip()
        tags_str = self.tags_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()
        
        if not title or not date or not content:
            messagebox.showerror("エラー", "タイトル、日付、内容は必須です")
            return
            
        # タグを配列に変換
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # 抜粋を生成
        excerpt = content[:100] + '...' if len(content) > 100 else content
        excerpt = excerpt.replace('\n', ' ')
        
        # 投稿データ作成
        post = {
            'id': f"{date}-{int(datetime.now().timestamp())}",
            'date': date,
            'title': title,
            'content': content,
            'excerpt': excerpt,
            'tags': tags
        }
        
        # 既存投稿の更新または新規追加
        existing_index = None
        for i, existing_post in enumerate(self.posts):
            if existing_post['title'] == title and existing_post['date'] == date:
                existing_index = i
                break
                
        if existing_index is not None:
            self.posts[existing_index] = post
            self.log(f"投稿を更新しました: {title}")
        else:
            self.posts.append(post)
            self.log(f"新規投稿を追加しました: {title}")
            
        # データ保存
        self.save_posts_to_json()
        self.update_blog_js()
        self.refresh_posts_list()
        
        # 自動プッシュ
        if self.auto_push_var.get():
            self.git_push()
            
    def delete_post(self):
        """投稿削除"""
        selection = self.posts_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "削除する投稿を選択してください")
            return
            
        if messagebox.askyesno("確認", "選択した投稿を削除しますか？"):
            index = selection[0]
            post = sorted(self.posts, key=lambda x: x['date'], reverse=True)[index]
            
            # リストから削除
            self.posts = [p for p in self.posts if p['id'] != post['id']]
            
            self.log(f"投稿を削除しました: {post['title']}")
            
            # データ保存
            self.save_posts_to_json()
            self.update_blog_js()
            self.refresh_posts_list()
            self.new_post()  # フォームクリア
            
            # 自動プッシュ
            if self.auto_push_var.get():
                self.git_push()
                
    def insert_image(self):
        """画像挿入"""
        files = filedialog.askopenfilenames(
            title="画像を選択",
            filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.gif *.webp")]
        )
        
        for file_path in files:
            # 画像をimagesディレクトリにコピー
            filename = os.path.basename(file_path)
            dest_path = os.path.join(self.images_dir, filename)
            
            try:
                shutil.copy2(file_path, dest_path)
                
                # Markdownリンクを挿入
                image_link = f"![{filename}](images/{filename})"
                self.content_text.insert(tk.INSERT, image_link + "\n\n")
                
                self.log(f"画像を挿入しました: {filename}")
                
            except Exception as e:
                self.log(f"画像挿入エラー: {e}")
                
        # ギャラリー更新
        self.refresh_gallery()
        
    def upload_images(self):
        """画像アップロード"""
        files = filedialog.askopenfilenames(
            title="アップロードする画像を選択",
            filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.gif *.webp")]
        )
        
        for file_path in files:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(self.images_dir, filename)
            
            try:
                shutil.copy2(file_path, dest_path)
                self.log(f"画像をアップロードしました: {filename}")
            except Exception as e:
                self.log(f"画像アップロードエラー: {e}")
                
        # ギャラリー更新
        self.refresh_gallery()
        
        # 自動プッシュ
        if self.auto_push_var.get():
            self.git_push()
            
    def refresh_gallery(self):
        """ギャラリー更新"""
        # 既存の画像ウィジェットを削除
        for widget in self.gallery_content_frame.winfo_children():
            widget.destroy()
            
        # 画像ファイル一覧取得
        image_files = []
        if os.path.exists(self.images_dir):
            for filename in os.listdir(self.images_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    image_files.append(filename)
                    
        # 画像を表示
        row = 0
        col = 0
        max_cols = 4
        
        for filename in sorted(image_files):
            file_path = os.path.join(self.images_dir, filename)
            
            try:
                # 画像読み込みとリサイズ
                img = Image.open(file_path)
                img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # 画像フレーム作成
                img_frame = ttk.Frame(self.gallery_content_frame)
                img_frame.grid(row=row, column=col, padx=5, pady=5)
                
                # 画像ラベル
                img_label = tk.Label(img_frame, image=photo)
                img_label.image = photo  # 参照を保持
                img_label.grid(row=0, column=0)
                
                # ファイル名ラベル
                name_label = tk.Label(img_frame, text=filename, wraplength=150)
                name_label.grid(row=1, column=0)
                
                # 削除ボタン
                del_btn = ttk.Button(img_frame, text="削除", 
                                   command=lambda f=filename: self.delete_image(f))
                del_btn.grid(row=2, column=0, pady=2)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
                    
            except Exception as e:
                self.log(f"画像表示エラー ({filename}): {e}")
                
        # スクロール領域更新
        self.gallery_content_frame.update_idletasks()
        self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))
        
    def delete_image(self, filename):
        """画像削除"""
        if messagebox.askyesno("確認", f"画像 '{filename}' を削除しますか？"):
            file_path = os.path.join(self.images_dir, filename)
            try:
                os.remove(file_path)
                self.log(f"画像を削除しました: {filename}")
                self.refresh_gallery()
                
                # 自動プッシュ
                if self.auto_push_var.get():
                    self.git_push()
                    
            except Exception as e:
                self.log(f"画像削除エラー: {e}")
                
    def git_push(self):
        """Gitプッシュ"""
        try:
            self.log("Gitにプッシュ中...")
            
            # git add .
            result = subprocess.run(["git", "add", "."], 
                                  cwd=self.project_path, 
                                  capture_output=True, text=True)
            
            # git commit
            commit_msg = f"Update content - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            result = subprocess.run(["git", "commit", "-m", commit_msg], 
                                  cwd=self.project_path, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0 or "nothing to commit" in result.stdout:
                # git push
                result = subprocess.run(["git", "push", "origin", "main"], 
                                      cwd=self.project_path, 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log("✅ Gitプッシュが完了しました")
                else:
                    self.log(f"❌ Gitプッシュエラー: {result.stderr}")
            else:
                self.log("📝 コミットする変更がありません")
                
        except Exception as e:
            self.log(f"❌ Gitプッシュエラー: {e}")
            
    def manual_push(self):
        """手動プッシュ"""
        self.git_push()
        
    def check_git_status(self):
        """Git状態確認"""
        try:
            result = subprocess.run(["git", "status"], 
                                  cwd=self.project_path, 
                                  capture_output=True, text=True)
            self.log("📊 Git状態:")
            self.log(result.stdout)
        except Exception as e:
            self.log(f"Git状態確認エラー: {e}")

def main():
    root = tk.Tk()
    app = HPAdminTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()