// Simple Blog System - Static Content Reader
class SimpleBlogSystem {
    constructor() {
        this.posts = [];
        this.loadStaticPosts();
    }

    // Load static posts from markdown files or JSON
    loadStaticPosts() {
        // For now, use static sample posts
        // In the future, this could read from a posts.json file
        this.posts = [
            {
                id: '2025-01-18',
                date: '2025-01-18',
                title: '冬の散歩で見つけた風景',
                content: '今日は久しぶりに晴れたので、カメラを持って近所を散歩してきました。冬の澄んだ空気の中で、いつもとは違う景色が広がっていました。\n\n公園の池には薄い氷が張っていて、朝日がキラキラと反射していました。木々の枝には霜が降りて、まるで銀細工のよう。\n\n写真を撮りながら、自然の美しさに改めて気づかされました。日常の中にも、こんな素敵な瞬間があるんですね。',
                excerpt: '今日は久しぶりに晴れたので、カメラを持って近所を散歩してきました。冬の澄んだ空気の中で、いつもとは違う景色が広がっていました。',
                tags: ['写真', '散歩', '自然']
            },
            {
                id: '2025-01-15',
                date: '2025-01-15',
                title: '新しいカメラを購入しました',
                content: 'ずっと欲しかったミラーレスカメラをついに手に入れました！\n\n選んだのは、軽量で持ち運びやすいモデル。これからもっと写真を撮りに出かけたくなります。\n\n早速、部屋の中でテスト撮影をしてみましたが、画質の良さに感動。特に暗い場所での撮影性能が素晴らしいです。\n\n週末は新しいカメラを持って、撮影旅行に出かける予定です。',
                excerpt: 'ずっと欲しかったミラーレスカメラをついに手に入れました！選んだのは、軽量で持ち運びやすいモデル。これからもっと写真を撮りに出かけたくなります。',
                tags: ['カメラ', '写真', '買い物']
            },
            {
                id: '2025-01-10',
                date: '2025-01-10',
                title: '2025年の目標',
                content: '新年あけましておめでとうございます。\n\n今年の目標を立てたので、ここに記録しておきます。\n\n1. 写真スキルの向上\n   - 月に最低1回は撮影旅行に行く\n   - オンライン写真講座を受講する\n\n2. ブログの定期更新\n   - 週に2回は更新する\n   - 写真と文章のクオリティを上げる\n\n3. 健康的な生活\n   - 毎日30分は散歩する\n   - 早寝早起きを心がける\n\n今年も素敵な一年になりますように！',
                excerpt: '新年あけましておめでとうございます。今年の目標を立てたので、ここに記録しておきます。写真スキルの向上、ブログの定期更新、健康的な生活。',
                tags: ['目標', '新年', '計画']
            }
        ];
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
}

// Contact Form Handler
class ContactForm {
    constructor() {
        this.setupForm();
    }

    setupForm() {
        const form = document.getElementById('contactForm');
        if (form) {
            form.addEventListener('submit', this.handleSubmit.bind(this));
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            message: formData.get('message')
        };

        try {
            // Use a service like Formspree, Netlify Forms, or EmailJS
            await this.sendEmail(data);
            this.showSuccessMessage();
            e.target.reset();
        } catch (error) {
            this.showErrorMessage();
        }
    }

    async sendEmail(data) {
        // Example using Formspree (you'll need to sign up and get an endpoint)
        const response = await fetch('https://formspree.io/f/YOUR_FORM_ID', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Failed to send email');
        }
    }

    showSuccessMessage() {
        const message = document.createElement('div');
        message.className = 'success-message';
        message.textContent = 'メッセージが送信されました。ありがとうございます！';
        message.style.cssText = 'background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin: 10px 0;';
        
        const form = document.getElementById('contactForm');
        form.parentNode.insertBefore(message, form);
        
        setTimeout(() => message.remove(), 5000);
    }

    showErrorMessage() {
        const message = document.createElement('div');
        message.className = 'error-message';
        message.textContent = 'メッセージの送信に失敗しました。もう一度お試しください。';
        message.style.cssText = 'background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin: 10px 0;';
        
        const form = document.getElementById('contactForm');
        form.parentNode.insertBefore(message, form);
        
        setTimeout(() => message.remove(), 5000);
    }
}

// Initialize
const blog = new SimpleBlogSystem();
const contactForm = new ContactForm();

// Export for use in other files
window.SimpleBlogSystem = SimpleBlogSystem;
window.ContactForm = ContactForm;
window.blog = blog;