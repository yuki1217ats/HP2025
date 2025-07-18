// GitHub API Image Upload System
class GitHubImageUploader {
    constructor() {
        this.repo = 'yuki1217ats/HP2025';
        this.branch = 'main';
        this.token = this.getStoredToken();
        this.imageFolder = 'images';
    }

    // Get stored GitHub token
    getStoredToken() {
        return localStorage.getItem('github_token');
    }

    // Set GitHub token
    setToken(token) {
        localStorage.setItem('github_token', token);
        this.token = token;
    }

    // Check if token is set
    hasToken() {
        return !!this.token;
    }

    // Generate unique filename
    generateFilename(originalName) {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        const extension = originalName.split('.').pop().toLowerCase();
        return `${timestamp}_${random}.${extension}`;
    }

    // Convert file to base64
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                // Remove data:image/jpeg;base64, prefix
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    // Upload image to GitHub
    async uploadImage(file) {
        if (!this.hasToken()) {
            throw new Error('GitHub token not set');
        }

        const filename = this.generateFilename(file.name);
        const base64Content = await this.fileToBase64(file);

        const url = `https://api.github.com/repos/${this.repo}/contents/${this.imageFolder}/${filename}`;
        
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Authorization': `token ${this.token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            },
            body: JSON.stringify({
                message: `Add image ${filename}`,
                content: base64Content,
                branch: this.branch
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`GitHub API Error: ${error.message}`);
        }

        const result = await response.json();
        // Use raw GitHub URL for direct image access
        const rawUrl = `https://raw.githubusercontent.com/${this.repo}/${this.branch}/${this.imageFolder}/${filename}`;
        return {
            filename: filename,
            url: rawUrl,
            path: result.content.path,
            download_url: result.content.download_url
        };
    }

    // Get all images from repository
    async getImages() {
        const url = `https://api.github.com/repos/${this.repo}/contents/${this.imageFolder}`;
        
        try {
            const response = await fetch(url, {
                headers: {
                    'Accept': 'application/vnd.github.v3+json'
                }
            });

            if (!response.ok) {
                return [];
            }

            const files = await response.json();
            return files.filter(file => 
                file.type === 'file' && 
                /\.(jpg|jpeg|png|gif|webp)$/i.test(file.name)
            ).map(file => ({
                name: file.name,
                url: `https://raw.githubusercontent.com/${this.repo}/${this.branch}/${this.imageFolder}/${file.name}`,
                download_url: file.download_url,
                path: file.path
            }));
        } catch (error) {
            console.error('Error fetching images:', error);
            return [];
        }
    }

    // Delete image from repository
    async deleteImage(filename) {
        if (!this.hasToken()) {
            throw new Error('GitHub token not set');
        }

        // First get the file to get its SHA
        const getUrl = `https://api.github.com/repos/${this.repo}/contents/${this.imageFolder}/${filename}`;
        const getResponse = await fetch(getUrl, {
            headers: {
                'Authorization': `token ${this.token}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        });

        if (!getResponse.ok) {
            throw new Error('Image not found');
        }

        const fileInfo = await getResponse.json();

        // Delete the file
        const deleteUrl = `https://api.github.com/repos/${this.repo}/contents/${this.imageFolder}/${filename}`;
        const deleteResponse = await fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'Authorization': `token ${this.token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            },
            body: JSON.stringify({
                message: `Delete image ${filename}`,
                sha: fileInfo.sha,
                branch: this.branch
            })
        });

        if (!deleteResponse.ok) {
            const error = await deleteResponse.json();
            throw new Error(`GitHub API Error: ${error.message}`);
        }

        return true;
    }

    // Create token setup dialog
    createTokenDialog() {
        return `
            <div class="token-overlay">
                <div class="token-container">
                    <h2>GitHub Token 設定</h2>
                    <p>画像アップロードにはGitHub Personal Access Tokenが必要です。</p>
                    
                    <div class="token-steps">
                        <h3>設定手順:</h3>
                        <ol>
                            <li><a href="https://github.com/settings/tokens" target="_blank">GitHub Settings → Developer settings → Personal access tokens</a></li>
                            <li>「Generate new token (classic)」をクリック</li>
                            <li>Note: 「HP2025 Image Upload」</li>
                            <li>Expiration: 「No expiration」または適切な期限</li>
                            <li>Scopes: 「repo」にチェック</li>
                            <li>「Generate token」をクリック</li>
                            <li>生成されたトークンをコピーして下記に貼り付け</li>
                        </ol>
                    </div>
                    
                    <form id="tokenForm">
                        <div class="form-group">
                            <label for="githubToken">GitHub Token</label>
                            <input type="password" id="githubToken" placeholder="ghp_..." required>
                        </div>
                        <div class="form-actions">
                            <button type="button" onclick="closeTokenDialog()" class="btn btn-secondary">キャンセル</button>
                            <button type="submit" class="btn btn-primary">保存</button>
                        </div>
                    </form>
                </div>
            </div>
            <style>
                .token-overlay {
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
                
                .token-container {
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                    max-width: 600px;
                    width: 100%;
                    margin: 20px;
                    max-height: 80vh;
                    overflow-y: auto;
                }
                
                .token-steps {
                    margin: 20px 0;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 4px;
                }
                
                .token-steps ol {
                    margin: 10px 0;
                    padding-left: 20px;
                }
                
                .token-steps li {
                    margin: 5px 0;
                }
                
                .token-steps a {
                    color: #1d3557;
                    text-decoration: none;
                }
                
                .token-steps a:hover {
                    text-decoration: underline;
                }
                
                .form-actions {
                    display: flex;
                    gap: 10px;
                    justify-content: flex-end;
                    margin-top: 20px;
                }
            </style>
        `;
    }
}

// Export for use in other files
window.GitHubImageUploader = GitHubImageUploader;