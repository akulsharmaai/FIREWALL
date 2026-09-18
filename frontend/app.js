/**
 * Human Firewall - Client-Side Interactive Engine
 * Handles navigation, mobile drawer, interactive security telemetry, and API hooks.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Drawer
  const openMenuBtn = document.getElementById('open-menu-btn');
  const closeMenuBtn = document.getElementById('close-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  const openDrawer = () => {
    if (!mobileMenu) return;
    mobileMenu.classList.remove('hidden', 'pointer-events-none');
    mobileMenu.classList.remove('opacity-0');
    mobileMenu.classList.add('opacity-100');
    document.body.style.overflow = 'hidden';
  };

  const closeDrawer = () => {
    if (!mobileMenu) return;
    mobileMenu.classList.add('opacity-0');
    mobileMenu.classList.add('pointer-events-none');
    setTimeout(() => {
      mobileMenu.classList.add('hidden');
      document.body.style.overflow = '';
    }, 250);
  };

  if (openMenuBtn) openMenuBtn.addEventListener('click', openDrawer);
  if (closeMenuBtn) closeMenuBtn.addEventListener('click', closeDrawer);
  mobileLinks.forEach(link => link.addEventListener('click', closeDrawer));

  // 2. Smooth Scrolling for Navigation
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (!targetId || targetId === '#') return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // 3. Interactive Notification Toast System
  const showToast = (message, type = 'info') => {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'fixed bottom-6 right-6 z-50 flex flex-col gap-3 pointer-events-none';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const colorClasses = type === 'success' 
      ? 'border-emerald-500/50 bg-slate-900/95 text-emerald-300' 
      : 'border-sky-500/50 bg-slate-900/95 text-sky-300';

    toast.className = `flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-md shadow-2xl text-xs font-mono transition-all duration-300 transform translate-y-4 opacity-0 pointer-events-auto ${colorClasses}`;
    toast.innerHTML = `
      <span class="w-2 h-2 rounded-full ${type === 'success' ? 'bg-emerald-400 animate-ping' : 'bg-sky-400 animate-ping'}"></span>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-4', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
    });

    setTimeout(() => {
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  };

  // 4. Interactive Shield Toggles
  document.querySelectorAll('.shield-toggle').forEach(toggle => {
    toggle.addEventListener('click', function () {
      const isActive = this.getAttribute('data-active') === 'true';
      const indicator = this.querySelector('span');
      const label = this.closest('div').querySelector('span').textContent;

      if (isActive) {
        this.setAttribute('data-active', 'false');
        this.classList.remove('bg-sky-500');
        this.classList.add('bg-slate-700');
        indicator.classList.remove('translate-x-4');
        indicator.classList.add('translate-x-0.5');
        showToast(`⚠️ ${label} disabled`, 'info');
      } else {
        this.setAttribute('data-active', 'true');
        this.classList.remove('bg-slate-700');
        this.classList.add('bg-sky-500');
        indicator.classList.remove('translate-x-0.5');
        indicator.classList.add('translate-x-4');
        showToast(`🛡️ ${label} re-enabled & active`, 'success');
      }
    });
  });

  // 5. Connect Demo Buttons
  const installBtn = document.getElementById('add-to-browser-btn');
  if (installBtn) {
    installBtn.addEventListener('click', () => {
      showToast('🚀 Extension package ready. Load unpacked from /extension directory!', 'success');
    });
  }

  document.querySelectorAll('button').forEach(btn => {
    if (btn.textContent.trim().toLowerCase().includes('log in')) {
      btn.addEventListener('click', () => {
        showToast('🔑 Authentication module ready for backend OAuth/JWT integration.', 'info');
      });
    }
  });

  // 6. Floating Badge Feedback in How It Works
  const badges = document.querySelectorAll('#how-it-works .animate-tech-float');
  badges.forEach(badge => {
    badge.style.cursor = 'pointer';
    badge.addEventListener('click', () => {
      const text = badge.textContent.trim();
      showToast(`Active Heuristic Rule: ${text}`, 'info');
    });
  });

  // 7. Backend API Health Check
  const checkBackendHealth = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        console.log('[Human Firewall] Connected to security backend API');
      }
    } catch (e) {
      console.log('[Human Firewall] Frontend running in standalone mode (FastAPI backend offline)');
    }
  };
  checkBackendHealth();

  console.log('[Human Firewall] Interactive UI Initialized successfully.');
});
