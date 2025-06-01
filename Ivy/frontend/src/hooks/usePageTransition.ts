import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export function usePageTransition() {
  const location = useLocation();

  useEffect(() => {
    // Scroll to top on page change
    window.scrollTo(0, 0);

    // Add a class to the body for page-specific animations
    document.body.classList.add('page-transition');
    document.body.classList.add(`page-${location.pathname.split('/')[1] || 'home'}`);

    return () => {
      document.body.classList.remove('page-transition');
      document.body.classList.remove(`page-${location.pathname.split('/')[1] || 'home'}`);
    };
  }, [location]);

  return location;
} 