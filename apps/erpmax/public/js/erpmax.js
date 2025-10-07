/* ERPMAX Custom JavaScript - 2025 Edition */

// ERPMAX Namespace
window.ERPMAX = {
    version: '1.0.0',
    settings: {},
    utils: {},
    ui: {},
    api: {}
};

// Initialize ERPMAX when DOM is ready
$(document).ready(function() {
    ERPMAX.init();
});

// Main initialization function
ERPMAX.init = function() {
    console.log('🚀 ERPMAX v' + ERPMAX.version + ' initialized');
    
    // Initialize components
    ERPMAX.ui.init();
    ERPMAX.utils.init();
    ERPMAX.setupEventHandlers();
    ERPMAX.enhanceUI();
};

// UI Enhancements
ERPMAX.ui.init = function() {
    // Add ERPMAX branding
    ERPMAX.ui.addBranding();
    
    // Enhance forms
    ERPMAX.ui.enhanceForms();
    
    // Add loading animations
    ERPMAX.ui.addLoadingAnimations();
    
    // Initialize tooltips
    ERPMAX.ui.initTooltips();
};

// Add ERPMAX branding
ERPMAX.ui.addBranding = function() {
    // Replace Frappe logo with ERPMAX logo
    setTimeout(function() {
        $('.navbar-brand img').attr('src', '/assets/erpmax/images/erpmax-logo.svg');
        $('.navbar-brand img').attr('alt', 'ERPMAX');
        
        // Update page title
        if (document.title.includes('Frappe')) {
            document.title = document.title.replace('Frappe', 'ERPMAX');
        }
        
        // Add ERPMAX class to body
        $('body').addClass('erpmax-app');
    }, 100);
};

// Enhance forms with modern styling
ERPMAX.ui.enhanceForms = function() {
    // Add floating labels
    $('.form-control').on('focus blur', function(e) {
        var $this = $(this);
        var label = $this.prev('label');
        
        if (e.type === 'focus' || this.value.length > 0) {
            label.addClass('floating');
        } else {
            label.removeClass('floating');
        }
    });
    
    // Enhanced form validation
    $('.form-control').on('input', function() {
        var $this = $(this);
        var isValid = this.checkValidity();
        
        $this.removeClass('is-valid is-invalid');
        
        if (this.value.length > 0) {
            $this.addClass(isValid ? 'is-valid' : 'is-invalid');
        }
    });
};

// Add loading animations
ERPMAX.ui.addLoadingAnimations = function() {
    // Intercept AJAX requests for loading indicators
    $(document).ajaxStart(function() {
        ERPMAX.ui.showLoading();
    }).ajaxStop(function() {
        ERPMAX.ui.hideLoading();
    });
};

// Show loading indicator
ERPMAX.ui.showLoading = function() {
    if (!$('.erpmax-loading').length) {
        var loadingHtml = `
            <div class="erpmax-loading" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, #1976D2, #42A5F5);
                z-index: 9999;
                animation: loading-bar 2s infinite;
            "></div>
        `;
        $('body').append(loadingHtml);
    }
};

// Hide loading indicator
ERPMAX.ui.hideLoading = function() {
    $('.erpmax-loading').fadeOut(300, function() {
        $(this).remove();
    });
};

// Initialize tooltips
ERPMAX.ui.initTooltips = function() {
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
};

// Utility functions
ERPMAX.utils.init = function() {
    // Add utility methods
    ERPMAX.utils.formatCurrency = function(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    };
    
    ERPMAX.utils.formatDate = function(date, format = 'short') {
        return new Intl.DateTimeFormat('en-US', {
            dateStyle: format
        }).format(new Date(date));
    };
    
    ERPMAX.utils.debounce = function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };
};

// API utilities
ERPMAX.api.call = function(method, args = {}, callback = null) {
    return frappe.call({
        method: method,
        args: args,
        callback: function(response) {
            if (callback) {
                callback(response);
            }
        },
        error: function(error) {
            console.error('ERPMAX API Error:', error);
            ERPMAX.ui.showError('An error occurred. Please try again.');
        }
    });
};

// Enhanced error handling
ERPMAX.ui.showError = function(message) {
    frappe.msgprint({
        title: 'Error',
        message: message,
        indicator: 'red'
    });
};

ERPMAX.ui.showSuccess = function(message) {
    frappe.msgprint({
        title: 'Success',
        message: message,
        indicator: 'green'
    });
};

// Setup event handlers
ERPMAX.setupEventHandlers = function() {
    // Handle navigation clicks
    $(document).on('click', '.erpmax-nav-item', function(e) {
        $('.erpmax-nav-item').removeClass('active');
        $(this).addClass('active');
    });
    
    // Handle form submissions
    $(document).on('submit', '.erpmax-form', function(e) {
        e.preventDefault();
        ERPMAX.handleFormSubmit($(this));
    });
    
    // Handle search
    $(document).on('input', '.erpmax-search', ERPMAX.utils.debounce(function() {
        ERPMAX.handleSearch($(this).val());
    }, 300));
};

// Handle form submission
ERPMAX.handleFormSubmit = function(form) {
    var formData = new FormData(form[0]);
    ERPMAX.ui.showLoading();
    
    // Process form data
    setTimeout(function() {
        ERPMAX.ui.hideLoading();
        ERPMAX.ui.showSuccess('Form submitted successfully!');
    }, 1000);
};

// Handle search
ERPMAX.handleSearch = function(query) {
    if (query.length < 3) return;
    
    console.log('Searching for:', query);
    // Implement search logic here
};

// Enhanced UI features
ERPMAX.enhanceUI = function() {
    // Add fade-in animations to cards
    $('.dashboard-card, .frappe-card').addClass('fade-in-up');
    
    // Enhanced hover effects
    $('.btn').hover(
        function() {
            $(this).addClass('btn-hover');
        },
        function() {
            $(this).removeClass('btn-hover');
        }
    );
    
    // Add ripple effect to buttons
    $('.btn').on('click', function(e) {
        var ripple = $('<span class="ripple"></span>');
        var btnOffset = $(this).offset();
        var xPos = e.pageX - btnOffset.left;
        var yPos = e.pageY - btnOffset.top;
        
        ripple.css({
            left: xPos,
            top: yPos
        });
        
        $(this).append(ripple);
        
        setTimeout(function() {
            ripple.remove();
        }, 600);
    });
};

// Keyboard shortcuts
$(document).keydown(function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.which === 75) {
        e.preventDefault();
        $('.search-bar input').focus();
    }
    
    // Ctrl/Cmd + Shift + N for new document
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.which === 78) {
        e.preventDefault();
        // Trigger new document creation
        if (cur_frm) {
            cur_frm.add_new();
        }
    }
});

// Performance monitoring
ERPMAX.performance = {
    start: performance.now(),
    
    mark: function(name) {
        performance.mark('erpmax-' + name);
    },
    
    measure: function(name, start, end) {
        performance.measure('erpmax-' + name, 'erpmax-' + start, 'erpmax-' + end);
    },
    
    getMetrics: function() {
        return performance.getEntriesByType('measure').filter(entry => 
            entry.name.startsWith('erpmax-')
        );
    }
};

// Add CSS for animations
if (!document.querySelector('#erpmax-animations')) {
    var style = document.createElement('style');
    style.id = 'erpmax-animations';
    style.textContent = `
        @keyframes loading-bar {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(100%); }
            100% { transform: translateX(100%); }
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .btn-hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    `;
    document.head.appendChild(style);
}

// Export ERPMAX for global access
window.ERPMAX = ERPMAX;

console.log('✨ ERPMAX JavaScript loaded successfully!');
