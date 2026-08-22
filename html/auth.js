const Auth = {
  getUser() {
    try {
      const user = localStorage.getItem('dosewise_user');
      return user ? JSON.parse(user) : null;
    } catch (e) {
      return null;
    }
  },

  setUser(userData) {
    localStorage.setItem('dosewise_user', JSON.stringify(userData));
  },

  login(name = 'User', email = '') {
    const user = { name, email, loggedInAt: new Date().toISOString() };
    this.setUser(user);
    window.location.href = '/home';
  },

  logout() {
    localStorage.removeItem('dosewise_user');
    window.location.href = '/';
  },

  requireAuth() {
    const user = this.getUser();
    if (!user) {
      window.location.href = '/login';
      return false;
    }
    return true;
  },

  initNavbar() {
    const user = this.getUser();
    const navLinks = document.querySelector('.nav-links');
    if (navLinks && user) {
      const loginItem = Array.from(navLinks.children).find(li => li.querySelector('a[href="/login"]'));
      if (loginItem) {
        loginItem.remove();
      }

      const userLi = document.createElement('li');
      userLi.className = 'user-nav-item';
      userLi.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; margin-left:6px;">
          <span style="font-size:0.85rem; font-weight:700; color:#0c7358; background:#eaf8f0; padding:6px 12px; border-radius:20px; border:1px solid #d9ece2; display:flex; align-items:center; gap:5px;">
            👤 ${this.escapeHtml(user.name)}
          </span>
          <button onclick="Auth.logout()" style="background:#fbeae8; color:#c0392b; border:1px solid #f2c9c2; border-radius:8px; padding:6px 12px; font-size:0.82rem; font-weight:700; cursor:pointer; font-family:inherit; transition:all 0.18s ease;">
            🚪 Logout
          </button>
        </div>
      `;
      navLinks.appendChild(userLi);
    }
  },

  escapeHtml(str) {
    const d = document.createElement('div');
    d.textContent = str || '';
    return d.innerHTML;
  }
};

// Auto check auth if page specifies protection
if (window.isProtectedPage) {
  if (Auth.requireAuth()) {
    document.addEventListener('DOMContentLoaded', () => {
      Auth.initNavbar();
    });
  }
}
