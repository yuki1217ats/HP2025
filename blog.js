// Blog Management System
class BlogSystem {
    constructor() {
        this.posts = this.loadPosts();
        this.currentPost = null;
        this.version = Date.now(); // Cache busting version
    }

    // Load posts from localStorage or JSON file
    loadPosts() {
        const saved = localStorage.getItem('blogPosts');
        if (saved) {
            return JSON.parse(saved);
        }
        
        // Default sample posts
        return [
            {
                id: '2025-01-18',
                date: '2025-01-18',
                title: '冬の散歩で見つけた風景',
                content: '今日は久しぶりに晴れたので、カメラを持って近所を散歩してきました。冬の澄んだ空気の中で、いつもとは違う景色が広がっていました。\n\n公園の池には薄い氷が張っていて、朝日がキラキラと反射していました。木々の枝には霜が降りて、まるで銀細工のよう。\n\n写真を撮りながら、自然の美しさに改めて気づかされました。日常の中にも、こんな素敵な瞬間があるんですね。',
                excerpt: '今日は久しぶりに晴れたので、カメラを持って近所を散歩してきました。冬の澄んだ空気の中で...',
                tags: ['写真', '散歩', '自然']
            },
            {
                id: '2025-01-15',
                date: '2025-01-15',
                title: '新しいカメラを購入しました',
                content: 'ずっと欲しかったミラーレスカメラをついに手に入れました！\n\n選んだのは、軽量で持ち運びやすいモデル。これからもっと写真を撮りに出かけたくなります。\n\n早速、部屋の中でテスト撮影をしてみましたが、画質の良さに感動。特に暗い場所での撮影性能が素晴らしいです。\n\n週末は新しいカメラを持って、撮影旅行に出かける予定です。',
                excerpt: 'ずっと欲しかったミラーレスカメラをついに手に入れました。これからもっと写真を...',
                tags: ['カメラ', '写真', '買い物']
            },
            {
                id: '2025-01-10',
                date: '2025-01-10',
                title: '2025年の目標',
                content: '新年あけましておめでとうございます。\n\n今年の目標を立てたので、ここに記録しておきます。\n\n1. 写真スキルの向上\n   - 月に最低1回は撮影旅行に行く\n   - オンライン写真講座を受講する\n\n2. ブログの定期更新\n   - 週に2回は更新する\n   - 写真と文章のクオリティを上げる\n\n3. 健康的な生活\n   - 毎日30分は散歩する\n   - 早寝早起きを心がける\n\n今年も素敵な一年になりますように！',
                excerpt: '新年あけましておめでとうございます。今年の目標を立てたので、ここに記録しておきます...',
                tags: ['目標', '新年', '計画']
            }
        ];
    }

    // Save posts to localStorage
    savePosts() {
        this.version = Date.now(); // Update version when saving
        localStorage.setItem('blogPosts', JSON.stringify(this.posts));
        localStorage.setItem('blogVersion', this.version.toString());
        
        // Trigger storage event for other tabs/windows
        window.dispatchEvent(new CustomEvent('blogUpdated', { 
            detail: { version: this.version } 
        }));
    }

    // Get all posts
    getAllPosts() {
        return this.posts.sort((a, b) => new Date(b.date) - new Date(a.date));
    }

    // Get posts for a specific month
    getPostsByMonth(year, month) {
        return this.posts.filter(post => {
            const postDate = new Date(post.date);
            return postDate.getFullYear() === year && postDate.getMonth() === month;
        });
    }

    // Get a single post by ID
    getPost(id) {
        return this.posts.find(post => post.id === id);
    }

    // Create a new post
    createPost(title, content, tags = []) {
        const date = new Date().toISOString().split('T')[0];
        const excerpt = content.substring(0, 100) + '...';
        
        const newPost = {
            id: date + '-' + Date.now(),
            date: date,
            title: title,
            content: content,
            excerpt: excerpt,
            tags: tags
        };
        
        this.posts.push(newPost);
        this.savePosts();
        return newPost;
    }

    // Update a post
    updatePost(id, updates) {
        const index = this.posts.findIndex(post => post.id === id);
        if (index !== -1) {
            this.posts[index] = { ...this.posts[index], ...updates };
            if (updates.content) {
                this.posts[index].excerpt = updates.content.substring(0, 100) + '...';
            }
            this.savePosts();
            return this.posts[index];
        }
        return null;
    }

    // Delete a post
    deletePost(id) {
        const index = this.posts.findIndex(post => post.id === id);
        if (index !== -1) {
            this.posts.splice(index, 1);
            this.savePosts();
            return true;
        }
        return false;
    }

    // Get posts with specific tag
    getPostsByTag(tag) {
        return this.posts.filter(post => post.tags.includes(tag));
    }

    // Get all unique tags
    getAllTags() {
        const tags = new Set();
        this.posts.forEach(post => {
            post.tags.forEach(tag => tags.add(tag));
        });
        return Array.from(tags);
    }
    
    // Check if data needs refresh
    needsRefresh() {
        const storedVersion = localStorage.getItem('blogVersion');
        return !storedVersion || parseInt(storedVersion) !== this.version;
    }
    
    // Refresh data from localStorage
    refreshData() {
        const newPosts = this.loadPosts();
        const newVersion = parseInt(localStorage.getItem('blogVersion') || '0');
        
        if (newVersion !== this.version) {
            this.posts = newPosts;
            this.version = newVersion;
            return true;
        }
        return false;
    }
}

// Initialize blog system
const blog = new BlogSystem();

// Export for use in other files
window.BlogSystem = BlogSystem;
window.blog = blog;