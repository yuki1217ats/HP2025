// Simple authentication system
class AuthSystem {
    constructor() {
        // In production, use a proper backend authentication
        // This is a simple demo using localStorage
        this.adminPasswordHash = this.getStoredHash() || this.hashPassword('admin123'); // Default password
        this.isAuthenticated = false;
        this.sessionTimeout = 30 * 60 * 1000; // 30 minutes
    }

    // Simple hash function (not secure for production)
    hashPassword(password) {
        let hash = 0;
        for (let i = 0; i < password.length; i++) {
            const char = password.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return hash.toString();
    }

    // Store password hash
    setPassword(newPassword) {
        const hash = this.hashPassword(newPassword);
        localStorage.setItem('adminPasswordHash', hash);
        this.adminPasswordHash = hash;
    }

    // Get stored hash
    getStoredHash() {
        return localStorage.getItem('adminPasswordHash');
    }

    // Check password
    checkPassword(password) {
        return this.hashPassword(password) === this.adminPasswordHash;
    }

    // Login
    login(password) {
        if (this.checkPassword(password)) {
            this.isAuthenticated = true;
            const sessionData = {
                authenticated: true,
                timestamp: Date.now()
            };
            sessionStorage.setItem('adminSession', JSON.stringify(sessionData));
            return true;
        }
        return false;
    }

    // Logout
    logout() {
        this.isAuthenticated = false;
        sessionStorage.removeItem('adminSession');
    }

    // Check session
    checkSession() {
        const sessionData = sessionStorage.getItem('adminSession');
        if (!sessionData) {
            return false;
        }

        const session = JSON.parse(sessionData);
        const now = Date.now();
        
        // Check if session is expired
        if (now - session.timestamp > this.sessionTimeout) {
            this.logout();
            return false;
        }

        // Update timestamp
        session.timestamp = now;
        sessionStorage.setItem('adminSession', JSON.stringify(session));
        this.isAuthenticated = true;
        return true;
    }

    // Create login form HTML
    createLoginForm() {
        return `
            <div class="auth-overlay">
                <div class="auth-container">
                    <h2>管理画面ログイン</h2>
                    <form id="loginForm">
                        <div class="form-group">
                            <label for="password">パスワード</label>
                            <input type="password" id="password" required autofocus>
                        </div>
                        <button type="submit" class="btn btn-primary">ログイン</button>
                    </form>
                </div>
            </div>
            <style>
                .auth-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10000;
                }
                
                .auth-container {
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                    max-width: 400px;
                    width: 100%;
                    margin: 20px;
                }
                
                .auth-container h2 {
                    margin-bottom: 30px;
                    text-align: center;
                    color: #333;
                }
                
                
                #loginForm .form-group {
                    margin-bottom: 20px;
                }
                
                #loginForm label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: 600;
                    color: #333;
                }
                
                #loginForm input {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                }
                
                #loginForm button {
                    width: 100%;
                    padding: 12px;
                    background: #1d3557;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                
                #loginForm button:hover {
                    background: #0a1929;
                }
                
                .auth-error {
                    color: #dc3545;
                    text-align: center;
                    margin-top: 10px;
                }
            </style>
        `;
    }
}

// Export
window.AuthSystem = AuthSystem;