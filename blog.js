// Simple Blog System - Static Content Reader
class SimpleBlogSystem {
    constructor() {
        this.posts = [
            {
                id: '2025-07-18',
                date: '2025-07-18',
                title: '宿泊',
                content: '羽田ファーストキャビンに宿泊
飛行機が遅れて22:00着だったので助かった。',
                excerpt: '羽田ファーストキャビン',
                tags: ['# 宿泊']
            }
        ];
        this.loadStaticPosts();
    }

    // Load static posts from markdown files or JSON
    loadStaticPosts() {
        // Posts are already loaded in constructor
        // This method can be used to refresh posts if needed
    }

    // Get all posts
    getAllPosts() {
        return this.posts.sort((a, b) => new Date(b.date) - new Date(a.date));
    }
    
    // Get a single post by ID
    getPost(id) {
        return this.posts.find(post => post.id === id);
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