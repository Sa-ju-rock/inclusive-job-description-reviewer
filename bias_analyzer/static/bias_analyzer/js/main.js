/**
 * JavaScript helper functions for EquiText - SDG 5 Bias-Free Reviewer
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alert notifications after 5 seconds
    const alerts = document.querySelectorAll('.alert-box');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });
});
