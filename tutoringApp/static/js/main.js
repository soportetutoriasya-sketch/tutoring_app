/**
 * TutoringApp Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {

    // ===== Dark Mode Toggle =====
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeIcon = document.getElementById('darkModeIcon');
    const body = document.body;

    // Load saved preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function () {
            const currentTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
            applyTheme(currentTheme);
            localStorage.setItem('theme', currentTheme);
        });
    }

    function applyTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            document.documentElement.setAttribute('data-bs-theme', 'dark');
            if (darkModeIcon) {
                darkModeIcon.classList.remove('bi-moon-fill');
                darkModeIcon.classList.add('bi-sun-fill');
            }
        } else {
            body.classList.remove('dark-mode');
            document.documentElement.setAttribute('data-bs-theme', 'light');
            if (darkModeIcon) {
                darkModeIcon.classList.remove('bi-sun-fill');
                darkModeIcon.classList.add('bi-moon-fill');
            }
        }
    }

    // ===== Leaflet Map Initialization =====
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        const defaultLat = parseFloat(mapContainer.dataset.lat) || 10.4806;
        const defaultLng = parseFloat(mapContainer.dataset.lng) || -66.9036;
        const defaultZoom = parseInt(mapContainer.dataset.zoom) || 13;

        const map = L.map('map').setView([defaultLat, defaultLng], defaultZoom);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19,
        }).addTo(map);

        // Load tutor markers if data attribute exists
        const tutorsDataEl = document.getElementById('tutors-data');
        if (tutorsDataEl) {
            try {
                const tutors = JSON.parse(tutorsDataEl.textContent);
                tutors.forEach(function (tutor) {
                    if (tutor.latitude && tutor.longitude) {
                        const marker = L.marker([tutor.latitude, tutor.longitude]).addTo(map);
                        marker.bindPopup(
                            '<strong>' + tutor.name + '</strong><br>' +
                            '<em>' + (tutor.subjects || '') + '</em><br>' +
                            (tutor.rating ? '&#11088; ' + tutor.rating + '/5' : '')
                        );
                    }
                });
            } catch (e) {
                console.error('Error loading tutor markers:', e);
            }
        }

        // Store map reference globally for other scripts
        window.tutoringMap = map;
    }

    // ===== AJAX Session Accept =====
    document.querySelectorAll('.btn-accept-session').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const sessionId = this.dataset.sessionId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch('/services/accept/' + sessionId + '/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    btn.textContent = 'Accepted';
                    btn.classList.remove('btn-success');
                    btn.classList.add('btn-secondary');
                    btn.disabled = true;
                    // Show success message
                    showAlert('Session accepted successfully!', 'success');
                } else {
                    showAlert(data.error || 'Failed to accept session.', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred. Please try again.', 'danger');
            });
        });
    });

    // ===== Alert Helper =====
    function showAlert(message, type) {
        const container = document.querySelector('.container');
        const alert = document.createElement('div');
        alert.className = 'alert alert-' + type + ' alert-dismissible fade show';
        alert.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
        container.insertBefore(alert, container.firstChild);
        setTimeout(function () {
            alert.remove();
        }, 5000);
    }

    // ===== CSRF Token for all AJAX requests =====
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Make CSRF token available globally
    window.csrfToken = getCookie('csrftoken');
});
