import { useState, useEffect } from 'react';

type ThemeMode = 'light' | 'dark';

export function useThemeMode() {
  const [mode, setMode] = useState<ThemeMode>(() => {
    const savedMode = localStorage.getItem('theme');
    return (savedMode as ThemeMode) || 'dark';
  });

  useEffect(() => {
    localStorage.setItem('theme', mode);
    document.documentElement.setAttribute('data-theme', mode);
    document.body.classList.toggle('dark-mode', mode === 'dark');
  }, [mode]);

  const toggleMode = () => {
    setMode(prevMode => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return { mode, toggleMode };
}
