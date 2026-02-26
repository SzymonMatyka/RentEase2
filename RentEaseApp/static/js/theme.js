// Theme management functionality
(function() {
    // Get theme from localStorage or default to light mode
    function getTheme() {
        return localStorage.getItem('theme') || 'light';
    }

    // Set theme
    function setTheme(theme) {
        localStorage.setItem('theme', theme);
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
        // Update toggle switch
        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            toggle.checked = (theme === 'dark');
        }
    }

    // Initialize theme on page load
    function initTheme() {
        const theme = getTheme();
        setTheme(theme);
    }

    // Toggle theme
    function toggleTheme() {
        const currentTheme = getTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }

    // Make toggleTheme available globally
    window.toggleTheme = toggleTheme;
})();

