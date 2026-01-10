// Portfolio filtering and interactions
(function() {
  'use strict';

  // Filter functionality
  const filterButtons = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('.portfolio-card');
  const noResultsMessage = document.getElementById('no-results');
  const portfolioGrid = document.getElementById('portfolio-grid');

  if (filterButtons.length > 0 && portfolioCards.length > 0) {
    filterButtons.forEach(button => {
      button.addEventListener('click', function() {
        const filter = this.getAttribute('data-filter');
        
        // Update active button
        filterButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        
        // Filter cards with smooth animation
        let visibleCount = 0;
        
        portfolioCards.forEach((card, index) => {
          const category = card.getAttribute('data-category');
          
          // Add exit animation
          card.style.animation = 'none';
          
          setTimeout(() => {
            if (filter === 'all' || category === filter) {
              card.style.display = 'flex';
              visibleCount++;
              // Stagger entrance animation
              setTimeout(() => {
                card.style.animation = `fadeIn 0.4s ease forwards ${index * 0.05}s`;
              }, 10);
            } else {
              card.style.display = 'none';
            }
            
            // Show/hide no results message
            if (visibleCount === 0) {
              noResultsMessage.style.display = 'block';
              portfolioGrid.style.display = 'none';
            } else {
              noResultsMessage.style.display = 'none';
              portfolioGrid.style.display = 'grid';
            }
          }, 150);
        });

        // Update URL parameter for shareability
        const url = new URL(window.location);
        if (filter === 'all') {
          url.searchParams.delete('category');
        } else {
          url.searchParams.set('category', filter);
        }
        window.history.replaceState({}, '', url);
      });
    });
  }

  // Apply filter from URL on page load
  window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');
    
    if (categoryParam) {
      const targetButton = document.querySelector(`[data-filter="${categoryParam}"]`);
      if (targetButton) {
        targetButton.click();
      }
    }
  });

  // Modal functionality for project details
  const modal = document.getElementById('project-modal');
  const modalBody = document.getElementById('modal-body');
  const portfolioCTAs = document.querySelectorAll('.portfolio-cta');

  if (modal && portfolioCTAs.length > 0) {
    portfolioCTAs.forEach(cta => {
      cta.addEventListener('click', function() {
        const card = this.closest('.portfolio-card');
        const title = card.querySelector('.portfolio-card-title').textContent;
        const location = card.querySelector('.portfolio-location').textContent;
        const description = card.querySelector('.portfolio-description').textContent;
        const imageSrc = card.querySelector('.portfolio-image').src;
        const imageAlt = card.querySelector('.portfolio-image').alt;
        const category = card.querySelector('.portfolio-category').textContent;

        // Populate modal with project details
        modalBody.innerHTML = `
          <div class="modal-project">
            <img src="${imageSrc}" alt="${imageAlt}" class="modal-image">
            <span class="modal-category">${category}</span>
            <h2 class="modal-title">${title}</h2>
            <p class="modal-location">${location}</p>
            <p class="modal-description">${description}</p>
            <div class="modal-details">
              <h3>Project Highlights</h3>
              <ul>
                <li>Professional craftsmanship and attention to detail</li>
                <li>Quality materials and expert installation</li>
                <li>Completed on time and within budget</li>
                <li>Exceptional customer satisfaction</li>
              </ul>
            </div>
            <div class="modal-cta">
              <p>Ready to start your own project?</p>
              <a href="/#contact" class="btn btn-primary">Get Your Free Quote</a>
            </div>
          </div>
        `;

        // Show modal with accessibility
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        
        // Focus management
        const closeButton = modal.querySelector('.modal-close');
        if (closeButton) closeButton.focus();
      });
    });
  }

  // Close modal function (global for inline onclick)
  window.closeModal = function() {
    if (modal) {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  };

  // Close modal on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      window.closeModal();
    }
  });

  // Reset filters function (global for inline onclick)
  window.resetFilters = function() {
    const allButton = document.querySelector('[data-filter="all"]');
    if (allButton) {
      allButton.click();
    }
  };

  // Lazy loading enhancement (if images have loading="lazy")
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          img.classList.add('loaded');
          observer.unobserve(img);
        }
      });
    }, {
      rootMargin: '50px'
    });

    document.querySelectorAll('.portfolio-image[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }

  // Smooth scroll to portfolio section from external links
  const hash = window.location.hash;
  if (hash === '#projects') {
    setTimeout(() => {
      const portfolioSection = document.querySelector('.portfolio-section');
      if (portfolioSection) {
        portfolioSection.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  }

  // Add animation on scroll for cards (optional enhancement)
  if ('IntersectionObserver' in window) {
    const cardObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    portfolioCards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      cardObserver.observe(card);
    });
  }

  // Keyboard navigation for filter buttons
  if (filterButtons.length > 0) {
    filterButtons.forEach((button, index) => {
      button.addEventListener('keydown', (e) => {
        let targetIndex;
        
        if (e.key === 'ArrowRight') {
          e.preventDefault();
          targetIndex = (index + 1) % filterButtons.length;
          filterButtons[targetIndex].focus();
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          targetIndex = (index - 1 + filterButtons.length) % filterButtons.length;
          filterButtons[targetIndex].focus();
        }
      });
    });
  }

})();
