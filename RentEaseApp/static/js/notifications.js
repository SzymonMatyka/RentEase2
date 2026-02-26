// Notification bell functionality
(function() {
    let notificationCheckInterval;
    const notificationsUrl = '/notifications';
    
    function updateNotificationBell() {
        fetch(notificationsUrl)
            .then(response => response.json())
            .then(data => {
                const bellIcon = document.getElementById('notificationBell');
                const badge = document.getElementById('notificationBadge');
                const dropdown = document.getElementById('notificationDropdown');
                
                if (badge) {
                    if (data.unread_count > 0) {
                        badge.textContent = data.unread_count > 99 ? '99+' : data.unread_count;
                        badge.style.display = 'flex';
                    } else {
                        badge.style.display = 'none';
                    }
                }
                
                // Update dropdown content
                if (dropdown && data.notifications) {
                    const list = dropdown.querySelector('.notification-list');
                    if (list) {
                        list.innerHTML = '';
                        
                        if (data.notifications.length === 0) {
                            list.innerHTML = '<div class="notification-item" style="padding: 15px; text-align: center; color: #666;">No new messages</div>';
                        } else {
                            data.notifications.forEach(notif => {
                                const item = document.createElement('div');
                                item.className = 'notification-item';
                                item.style.cursor = 'pointer';
                                item.onclick = () => {
                                    window.location.href = '/conversations/' + notif.conversation_id;
                                };
                                
                                const title = document.createElement('div');
                                title.className = 'notification-title';
                                title.textContent = notif.offer_title;
                                
                                const content = document.createElement('div');
                                content.className = 'notification-content';
                                content.textContent = notif.latest_message;
                                
                                const meta = document.createElement('div');
                                meta.className = 'notification-meta';
                                if (notif.tenant_name) {
                                    meta.textContent = 'From: ' + notif.tenant_name;
                                } else if (notif.landlord_name) {
                                    meta.textContent = 'From: ' + notif.landlord_name;
                                }
                                
                                item.appendChild(title);
                                item.appendChild(content);
                                item.appendChild(meta);
                                list.appendChild(item);
                            });
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching notifications:', error);
            });
    }
    
    function toggleDropdown() {
        const dropdown = document.getElementById('notificationDropdown');
        const bell = document.getElementById('notificationBell');
        if (dropdown && bell) {
            const isShowing = dropdown.classList.contains('show');
            dropdown.classList.toggle('show');
            
            if (!isShowing) {
                // Calculate position when showing
                const bellRect = bell.getBoundingClientRect();
                const dropdownRect = dropdown.getBoundingClientRect();
                
                // Position dropdown below the bell, aligned to the right
                dropdown.style.position = 'fixed';
                dropdown.style.top = (bellRect.bottom + window.scrollY + 10) + 'px';
                dropdown.style.right = (window.innerWidth - bellRect.right) + 'px';
                dropdown.style.left = 'auto';
            }
        }
    }
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const bell = document.getElementById('notificationBell');
        const dropdown = document.getElementById('notificationDropdown');
        if (bell && dropdown && !bell.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.classList.remove('show');
        }
    });
    
    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            const bell = document.getElementById('notificationBell');
            if (bell) {
                bell.addEventListener('click', function(e) {
                    e.stopPropagation();
                    toggleDropdown();
                });
            }
            updateNotificationBell();
            // Check for new notifications every 30 seconds
            notificationCheckInterval = setInterval(updateNotificationBell, 30000);
        });
    } else {
        const bell = document.getElementById('notificationBell');
        if (bell) {
            bell.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleDropdown();
            });
        }
        updateNotificationBell();
        notificationCheckInterval = setInterval(updateNotificationBell, 30000);
    }
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        if (notificationCheckInterval) {
            clearInterval(notificationCheckInterval);
        }
    });
    
    // Make functions available globally
    window.updateNotificationBell = updateNotificationBell;
})();

